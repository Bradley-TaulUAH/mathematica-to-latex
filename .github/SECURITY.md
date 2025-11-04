# Security Policy

## Supported Versions

This project is currently in active development. We support the latest version with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public issue
2. Email the maintainer directly (see GitHub profile for contact information)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge your report within 48 hours and provide updates on the resolution timeline.

## Security Considerations

This tool:
- Processes Mathematica notebook files which may contain arbitrary code
- Does NOT execute any Mathematica code - it only parses and converts text
- Reads input files and writes output files - ensure you trust your input sources
- Has no network access requirements
- Does not require elevated privileges

## Best Practices

When using this converter:
- Only process notebook files from trusted sources
- Review generated LaTeX before compiling (LaTeX can execute system commands)
- Keep your Python installation up to date
- Use in a sandboxed environment when processing untrusted notebooks
