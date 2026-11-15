from xml.etree.ElementTree import Element, SubElement, tostring

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse

JSON_TYPES = ("application/json",)
XML_TYPES = ("application/xml", "text/xml")


def _quality(accept_header: str, wanted: tuple) -> float:
    """Best 'q' value the Accept header gives to any of the wanted media types (0 = not accepted)."""
    best = 0.0
    wanted_groups = {w.split("/")[0] + "/*" for w in wanted}
    for part in accept_header.split(","):
        pieces = [p.strip() for p in part.split(";")]
        media = pieces[0].lower()
        q = 1.0
        for p in pieces[1:]:
            if p.lower().startswith("q="):
                try:
                    q = float(p[2:])
                except ValueError:
                    q = 0.0
        if media in wanted or media == "*/*" or media in wanted_groups:
            best = max(best, q)
    return best


def choose_format(request: Request) -> str:
    """Decide 'json' or 'xml' for the response.

    1. ?format=json or ?format=xml wins if present.
    2. Otherwise the Accept header decides (the one with the higher q value).
    3. With no preference at all, the answer is JSON.
    """
    fmt = request.query_params.get("format")
    if fmt is not None:
        fmt = fmt.strip().lower()
        if fmt not in ("json", "xml"):
            raise HTTPException(status_code=400, detail="The 'format' query parameter must be 'json' or 'xml'.")
        return fmt

    accept = request.headers.get("accept", "").strip()
    if not accept:
        return "json"
    q_json = _quality(accept, JSON_TYPES)
    q_xml = _quality(accept, XML_TYPES)
    if q_json == 0 and q_xml == 0:
        raise HTTPException(
            status_code=406,
            detail="Not Acceptable. This endpoint can answer with application/json or application/xml.",
        )
    return "xml" if q_xml > q_json else "json"


def _to_xml(record: dict, root_name: str = "candidate") -> str:
    root = Element(root_name)
    for key, value in record.items():
        child = SubElement(root, key)
        child.text = "" if value is None else str(value)
    # ElementTree escapes &, < and > in the text for us
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="unicode")


def build_response(request: Request, record: dict) -> Response:
    """Send 'record' back as JSON or XML, as the client asked."""
    record = {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in record.items()}
    headers = {"Vary": "Accept"}
    if choose_format(request) == "xml":
        return Response(content=_to_xml(record), media_type="application/xml", headers=headers)
    return JSONResponse(content=record, headers=headers)
