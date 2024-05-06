# Swagger Dereferncer

- Normal swagger files have references to ensure that common parts are shared across files instead of duplicating them.
- This is good for code readibility, but when it comes to LLM performance, it becomes difficult for it to understand the references.
- This dereferencer resolves all the references and then replaces the reference with the full json body.
- This will ensure that the LLM does not have to resolve references and can focus on understanding the complete swagger spec as a single json document.
