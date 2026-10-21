# Backend routing notes

VisualForge is a routing policy, not an image model. The actual generation capability comes from the host or a backend installed by the user.

## Host-provided tools

Use only tools explicitly exposed in the active session. Follow their supported formats, save-path rules, input-image rules, and usage limits. Do not assume a tool from a different chat product is available inside a CLI agent.

## Local generation

A local system such as ComfyUI can avoid per-image API charges, but still has hardware, setup, storage, electricity, and model-license considerations. Before using it, verify that the service is reachable and query the installed models/workflows rather than guessing names. Ask before downloading large files or installing custom nodes.

## External services

Use only if the user has configured or explicitly approved the service. Clarify that free tiers can have quotas, rate limits, terms, or change over time. Never claim a service is free forever.

## Code-native fallback

SVG/CSS/canvas are strong choices for diagrams, icons, patterns, simple illustrations, and interface graphics. They are not substitutes for photorealistic imagery. Explain the difference and match the fallback to the actual request.
