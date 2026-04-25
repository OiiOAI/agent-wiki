"""Agent-wiki ingest pipeline.

8-phase pipeline A→H:
  A pdf_to_md      B chunk        C extract       D compile
  E validate       F conflict     G report        H commit
"""
