"""Turns a Quote into plain-language text that explains every line."""
from .calculator import Quote
from .i18n import t
from .money import fmt


def explain_line(line, pricing: dict, lang: str) -> str:
    s = pricing["services"][line.service]
    name, unit = s[lang], line.unit
    qty = f"{line.quantity.normalize():f}"
    if line.overridden:
        who = "El dueño fijó este precio personalmente." if lang == "es" \
            else "The owner set this price personally."
        return (f"{name}: {qty} {unit} × {fmt(line.unit_price)} = {fmt(line.total)}. {who}")
    mat, hrs = fmt(line.material), f"{line.labor_hours.normalize():f}"
    return (_es if lang == "es" else _en)(line, name, unit, qty, mat, hrs)


def _en(line, name, unit, qty, mat, hrs):
    return (f"{name}: {qty} {unit} × {fmt(line.unit_price)} = {fmt(line.total)}. "
            f"Each {unit} covers materials ({mat}) and {hrs} labor hours, plus our overhead margin.")


def _es(line, name, unit, qty, mat, hrs):
    return (f"{name}: {qty} {unit} × {fmt(line.unit_price)} = {fmt(line.total)}. "
            f"Cada {unit} cubre materiales ({mat}) y {hrs} horas de trabajo, más nuestro margen operativo.")


def explain_quote(quote: Quote, pricing: dict, lang: str) -> str:
    lang = lang if lang in ("en", "es") else "en"
    out = [t("greeting", lang), ""]
    out += [f"• {explain_line(l, pricing, lang)}" for l in quote.lines]
    if quote.minimum_applied:
        out.append("• " + ("Se aplicó el cargo mínimo de visita." if lang == "es"
                           else "Our minimum service charge was applied."))
    out.append("")
    if lang == "es":
        out += [f"Subtotal: {fmt(quote.subtotal)}",
                f"Impuesto ({quote.tax_rate * 100:.2f}%): {fmt(quote.tax)}",
                f"Total: {fmt(quote.total)}", "",
                "Este es un estimado basado en su descripción y fotos; el precio final se confirma tras la visita."]
    else:
        out += [f"Subtotal: {fmt(quote.subtotal)}",
                f"Tax ({quote.tax_rate * 100:.2f}%): {fmt(quote.tax)}",
                f"Total: {fmt(quote.total)}", "",
                "This is an estimate based on your description and photos; the final price is confirmed after a site visit."]
    return "\n".join(out)
