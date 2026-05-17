from app.llm.grammar import day_response_grammar, schema_to_gbnf


def test_schema_to_gbnf_returns_string() -> None:
    schema = {"type": "object", "properties": {"foo": {"type": "string"}}}
    grammar = schema_to_gbnf(schema)
    assert "root" in grammar
    assert "object" in grammar


def test_day_response_grammar_includes_root() -> None:
    grammar = day_response_grammar()
    assert grammar.startswith("root")
    assert len(grammar) > 50
