# VERITAS — Import Graph

Every import in every runtime module, resolved.

## corpus_index.py
```
hashlib, json, os, re, sqlite3, datetime, pathlib  ← stdlib only
```

## gap_log.py
```
json, uuid, datetime, pathlib  ← stdlib only
```

## citation_graph.py
```
re, json, collections.OrderedDict, collections.deque  ← stdlib only
corpus_index  ← local
gap_log       ← local
```

## source_verifier.py
```
hashlib, json, os, re, sqlite3, datetime, pathlib, urllib.parse  ← stdlib only
```

## pipeline_runner.py
```
hashlib, json, os, re, collections, datetime, pathlib  ← stdlib only
corpus_index     ← local
gap_log          ← local
citation_graph   ← local
source_verifier  ← local (lazy)
report_generator ← local (lazy)
phone_contract   ← local (lazy)
config           ← local (lazy)
ai_integration   ← local (lazy)
document_processor ← local (lazy)
literal_dictionary ← local (lazy)
legal_dictionary   ← local (lazy)
consistency_engine ← local (lazy)
```

## report_generator.py
```
os, datetime  ← stdlib only
privacy_scrubber ← local
```

## phone_contract.py
```
hashlib, json, os, datetime, pathlib  ← stdlib only
```

## main.py
```
os, sys, re, threading, webbrowser, datetime  ← stdlib only
tkinter, tkinter.ttk, tkinter.scrolledtext   ← stdlib (needs python3-tk)
tkinter.filedialog, tkinter.messagebox       ← stdlib
config           ← local
pipeline_runner  ← local
report_generator ← local
ai_integration   ← local
document_processor ← local
legal_dictionary   ← local
literal_dictionary ← local
consistency_engine ← local
privacy_scrubber   ← local
```

## ai_integration.py
```
json, os, datetime  ← stdlib only
requests            ← third-party (pip install requests)
```

## document_processor.py
```
os, re, zipfile  ← stdlib only
pypdf            ← third-party (pip install pypdf)
docx             ← third-party (pip install python-docx)
```

## consistency_engine.py
```
os, re, subprocess, tempfile, difflib  ← stdlib only
faster_whisper   ← optional third-party
whisper          ← optional third-party
```

## metadata_stripper.py
```
os           ← stdlib only
PIL.Image    ← third-party (pip install Pillow)
mutagen      ← optional third-party
```

## privacy_scrubber.py
```
re  ← stdlib only
```

## legal_dictionary.py / literal_dictionary.py
```
(no imports — pure data)
```
