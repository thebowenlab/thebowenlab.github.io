"""
cite process to convert sources and metasources into full citations
"""

import traceback
from importlib import import_module
from pathlib import Path
from dotenv import load_dotenv
from util import *


# load environment variables
load_dotenv()


# save errors/warnings for reporting at end
errors = []
warnings = []

# output citations file
output_file = "_data/citations.yaml"


log()

log("Compiling sources")

# compiled list of sources
sources = []

# in-order list of plugins to run
# plugins = ["google-scholar", "pubmed", "orcid", "sources"]
plugins = ["sources"]

# loop through plugins
for plugin in plugins:
    # convert into path object
    plugin = Path(f"plugins/{plugin}.py")

    log(f"Running {plugin.stem} plugin")

    # get all data files to process with current plugin
    files = Path.cwd().glob(f"_data/{plugin.stem}*.*")
    files = list(filter(lambda p: p.suffix in [".yaml", ".yml", ".json"], files))

    log(f"Found {len(files)} {plugin.stem}* data file(s)", indent=1)

    # loop through data files
    for file in files:
        log(f"Processing data file {file.name}", indent=1)

        # load data from file
        try:
            data = load_data(file)
            # check if file in correct format
            if not list_of_dicts(data):
                raise Exception(f"{file.name} data file not a list of dicts")
        except Exception as e:
            log(e, indent=2, level="ERROR")
            errors.append(e)
            continue

        # loop through data entries
        for index, entry in enumerate(data):
            log(f"Processing entry {index + 1} of {len(data)}, {label(entry)}", level=2)

            # run plugin on data entry to expand into multiple sources
            try:
                expanded = import_module(f"plugins.{plugin.stem}").main(entry)
                # check that plugin returned correct format
                if not list_of_dicts(expanded):
                    raise Exception(f"{plugin.stem} plugin didn't return list of dicts")
            # catch any plugin error
            except Exception as e:
                # log detailed pre-formatted/colored trace
                print(traceback.format_exc())
                # log high-level error
                log(e, indent=3, level="ERROR")
                errors.append(e)
                continue

            # loop through sources
            for source in expanded:
                if plugin.stem != "sources":
                    log(label(source), level=3)

                # include meta info about source
                source["plugin"] = plugin.name
                source["file"] = file.name

                # add source to compiled list
                sources.append(source)

            if plugin.stem != "sources":
                log(f"{len(expanded)} source(s)", indent=3)

log("Merging sources by normalized id/title")


def _norm_text(s):
    """Normalize text for fuzzy-equality matching (titles)."""
    if s is None:
        return ""
    s = str(s).strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    # collapse punctuation/whitespace differences
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _extract_doi(s):
    """
    Extract canonical DOI string from many formats:
      - https://doi.org/10.xxxx/abc
      - http://dx.doi.org/10.xxxx/abc
      - doi:10.xxxx/abc
      - 10.xxxx/abc
    Returns lowercase DOI or "".
    """
    if not s:
        return ""
    s = str(s).strip()

    # Common DOI URL / prefix cleanup
    s_low = s.lower().strip()
    s_low = re.sub(r"^https?://(dx\.)?doi\.org/", "", s_low)
    s_low = re.sub(r"^doi:\s*", "", s_low)

    # If the whole thing is now a DOI, capture it
    # DOI generally begins with 10.<registrant>/<suffix>
    m = re.search(r"(10\.\d{4,9}/\S+)", s_low)
    if not m:
        return ""

    doi = m.group(1)

    # Strip trailing punctuation often introduced in copied references
    doi = doi.rstrip(").,;]")
    doi = doi.lstrip("(")

    return doi


def _canonical_id(source):
    """
    Build a normalized identity key for exact-ish matching.
    Prefers DOI normalization, otherwise falls back to normalized id.
    """
    raw_id = get_safe(source, "id", "")
    if not raw_id:
        return ""

    doi = _extract_doi(raw_id)
    if doi:
        return f"doi:{doi}"

    # Generic fallback (normalize whitespace/case)
    return f"id:{_norm_text(raw_id)}"


def _canonical_title(source):
    """
    Build a normalized title key for fallback matching.
    """
    title = get_safe(source, "title", "")
    return _norm_text(title)


def _plugin_priority(source):
    """
    Higher number = preferred source when merging conflicts.
    We generally want user-curated sources.py entries to win.
    """
    plugin = str(get_safe(source, "plugin", ""))
    # plugin is stored as file name, e.g. "sources.py", "orcid.py"
    if plugin == "sources.py":
        return 100
    if plugin == "orcid.py":
        return 50
    return 10


def _merge_two_sources(a, b):
    """
    Merge source dicts with preference for curated/manual entries.
    Preserves richer fields (e.g., image/buttons/tags) when present.
    """
    a = deepcopy(a)
    b = deepcopy(b)

    # choose base / overlay by plugin priority
    if _plugin_priority(b) > _plugin_priority(a):
        base, overlay = b, a
    else:
        base, overlay = a, b

    merged = deepcopy(base)

    # Merge fields from overlay carefully
    for k, v in overlay.items():
        if v in [None, "", [], {}]:
            continue

        # If base lacks value, take overlay
        if k not in merged or merged[k] in [None, "", [], {}]:
            merged[k] = v
            continue

        # Merge tags uniquely
        if k == "tags" and isinstance(merged[k], list) and isinstance(v, list):
            seen = set()
            out = []
            for item in merged[k] + v:
                key = str(item).strip().lower()
                if key not in seen:
                    seen.add(key)
                    out.append(item)
            merged[k] = out
            continue

        # Merge buttons uniquely by (type, text, link)
        if k == "buttons" and isinstance(merged[k], list) and isinstance(v, list):
            seen = set()
            out = []
            for btn in merged[k] + v:
                if isinstance(btn, dict):
                    sig = (
                        str(btn.get("type", "")).strip().lower(),
                        str(btn.get("text", "")).strip().lower(),
                        str(btn.get("link", "")).strip(),
                    )
                else:
                    sig = ("raw", str(btn))
                if sig not in seen:
                    seen.add(sig)
                    out.append(btn)
            merged[k] = out
            continue

        # Keep base value by default (because base was chosen by priority)
        # but you can add exceptions here if desired.

    return merged


# First pass: merge by canonical id
id_groups = {}
no_id_sources = []

for s in sources:
    key = _canonical_id(s)
    if key:
        id_groups.setdefault(key, []).append(s)
    else:
        no_id_sources.append(s)

merged_sources = []

for key, group in id_groups.items():
    if len(group) > 1:
        log(f"Found duplicate id-group {key} ({len(group)} entries)", indent=2)
    merged = group[0]
    for g in group[1:]:
        merged = _merge_two_sources(merged, g)
    merged_sources.append(merged)

# Include entries with no id as-is for now
merged_sources.extend(no_id_sources)

# Second pass: merge by normalized title (fallback)
# This will merge preprint/journal versions if titles match closely after normalization.
title_groups = {}
no_title_sources = []

for s in merged_sources:
    tkey = _canonical_title(s)
    if tkey:
        title_groups.setdefault(tkey, []).append(s)
    else:
        no_title_sources.append(s)

sources = []

for tkey, group in title_groups.items():
    if len(group) > 1:
        log(f"Found duplicate title-group '{tkey[:80]}' ({len(group)} entries)", indent=2)
    merged = group[0]
    for g in group[1:]:
        merged = _merge_two_sources(merged, g)
    sources.append(merged)

sources.extend(no_title_sources)


log(f"{len(sources)} total source(s) to cite")


log()

log("Generating citations")

# list of new citations
citations = []


# loop through compiled sources
for index, source in enumerate(sources):
    log(f"Processing source {index + 1} of {len(sources)}, {label(source)}")

    # if explicitly flagged, remove/ignore entry
    if get_safe(source, "remove", False) == True:
        continue

    # new citation data for source
    citation = {}

    # source id
    _id = get_safe(source, "id", "").strip()

    # manubot doesn't work without an id
    if _id:
        log("Using Manubot to generate citation", indent=1)

        try:
            # run manubot and set citation
            citation = cite_with_manubot(_id)

        # if manubot cannot cite source
        except Exception as e:
            plugin = get_safe(source, "plugin", "")
            file = get_safe(source, "file", "")
            # if regular source (id entered by user), throw error
            if plugin == "sources.py":
                log(e, indent=3, level="ERROR")
                errors.append(f"Manubot could not generate citation for source {_id}")
            # otherwise, if from metasource (id retrieved from some third-party api), just warn
            else:
                log(e, indent=3, level="WARNING")
                warnings.append(
                    f"Manubot could not generate citation for source {_id} (from {file} with {plugin})"
                )
                # discard source from citations
                continue

    # preserve fields from input source, overriding existing fields
    citation.update(source)

    # ensure date in proper format for correct date sorting
    if get_safe(citation, "date", ""):
        citation["date"] = format_date(get_safe(citation, "date", ""))

    # add new citation to list
    citations.append(citation)


log()

log("Saving updated citations")


# save new citations
try:
    save_data(output_file, citations)
except Exception as e:
    log(e, level="ERROR")
    errors.append(e)


log()


# exit at end, so user can see all errors/warnings in one run
if len(warnings):
    log(f"{len(warnings)} warning(s) occurred above", level="WARNING")
    for warning in warnings:
        log(warning, indent=1, level="WARNING")

if len(errors):
    log(f"{len(errors)} error(s) occurred above", level="ERROR")
    for error in errors:
        log(error, indent=1, level="ERROR")
    log()
    exit(1)

else:
    log("All done!", level="SUCCESS")

log()
