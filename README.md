# Byteview
Independent Luau bytecode inspection frontend. Upload these files at your GitHub repository root. On Render create a Blueprint from that repository using render.yaml. Set PUBLIC_URL to your deployed HTTPS origin (no trailing path) so the script calls the correct public address. GitHub Pages alone cannot run the Python API.

Local: `pip install -r requirements.txt` then `flask --app app run`.

Try Load sample → Run. The 22 exact reference fixtures work offline by lookup, not by running a local engine. Fixtures from boydev-1444/lunaux-decompiler, Apache 2.0; see LICENSE. Other inputs require the public LunaUX API and are subject to its availability and limits. Do not submit confidential bytecode. Add rate limiting before opening a large public instance.

GET /script returns a Luau module as plain text. In Roblox Studio, copy the reviewed text into a ModuleScript, require it from a server Script, enable HTTP requests, then call `client.decompile(base64Bytecode)` or `client.disassemble(base64Bytecode)`. Script client requests allow remote processing. It does not extract bytecode from live scripts. game:HttpGet is not a normal experience-script API.
