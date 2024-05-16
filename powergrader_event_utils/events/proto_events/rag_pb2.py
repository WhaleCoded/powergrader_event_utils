# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rag.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import powergrader_event_utils.events.proto_events.rag_chunks_pb2 as rag__chunks__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\trag.proto\x12\x03rag\x1a\x10rag_chunks.proto"\x9c\x01\n\x0e\x44ocumentSource\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nscope_uuid\x18\x04 \x01(\t\x12"\n\nscope_type\x18\x05 \x01(\x0e\x32\x0e.rag.ScopeType\x12\x19\n\x11version_timestamp\x18\x08 \x01(\x04"\xb7\x01\n\x12SupportingDocument\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x02 \x01(\t\x12\x1a\n\x12source_public_uuid\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x05 \x01(\t\x12 \n\tfile_type\x18\x06 \x01(\x0e\x32\r.rag.FileType\x12\x19\n\x11version_timestamp\x18\x07 \x01(\x04"\xa2\x01\n\x17\x44ocumentChunkingStarted\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x1d\n\x15\x64ocument_version_uuid\x18\x02 \x01(\t\x12\x17\n\x0frag_method_info\x18\x03 \x01(\t\x12(\n\rdocument_type\x18\x04 \x01(\x0e\x32\x11.rag.DocumentType\x12\x17\n\x0fstart_timestamp\x18\x05 \x01(\x04"\xa3\x01\n\x0e\x44ocumentChunks\x12&\n\x1e\x64ocument_chunking_started_uuid\x18\x01 \x01(\t\x12/\n\rdocument_root\x18\x02 \x01(\x0b\x32\x18.rag_chunks.DocumentRoot\x12!\n\x06\x63hunks\x18\x03 \x03(\x0b\x32\x11.rag_chunks.Chunk\x12\x15\n\rend_timestamp\x18\x04 \x01(\x04"\x8b\x01\n!DocumentChunkSummarizationStarted\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x1c\n\x14\x64ocument_chunks_uuid\x18\x02 \x01(\t\x12!\n\x19summarization_method_info\x18\x03 \x01(\t\x12\x17\n\x0fstart_timestamp\x18\x04 \x01(\x04"I\n\x0c\x43hunkSummary\x12\x12\n\nchunk_uuid\x18\x01 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x02 \x01(\t\x12\x0f\n\x07summary\x18\x03 \x01(\t"\x8e\x01\n\x16\x44ocumentChunkSummaries\x12\x31\n)document_chunk_summarization_started_uuid\x18\x01 \x01(\t\x12*\n\x0f\x63hunk_summaries\x18\x02 \x03(\x0b\x32\x11.rag.ChunkSummary\x12\x15\n\rend_timestamp\x18\x03 \x01(\x04"\xac\x01\n\x1f\x44ocumentPassageEmbeddingStarted\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x1c\n\x14\x64ocument_chunks_uuid\x18\x02 \x01(\t\x12%\n\x1d\x64ocument_chunk_summaries_uuid\x18\x03 \x01(\t\x12\x1d\n\x15\x65mbedding_method_info\x18\x04 \x01(\t\x12\x17\n\x0fstart_timestamp\x18\x05 \x01(\x04"\x1e\n\tEmbedding\x12\x11\n\tembedding\x18\x01 \x03(\x02"L\n\x10PassageEmbedding\x12\x14\n\x0cpassage_uuid\x18\x01 \x01(\t\x12"\n\nembeddings\x18\x03 \x03(\x0b\x32\x0e.rag.Embedding"\x96\x01\n\x19\x44ocumentPassageEmbeddings\x12/\n\'document_passage_embedding_started_uuid\x18\x01 \x01(\t\x12\x31\n\x12passage_embeddings\x18\x02 \x03(\x0b\x32\x15.rag.PassageEmbedding\x12\x15\n\rend_timestamp\x18\x03 \x01(\x04*d\n\tScopeType\x12\x11\n\rUNKNOWN_SCOPE\x10\x00\x12\x14\n\x10\x41SSIGNMENT_SCOPE\x10\x01\x12\x10\n\x0c\x43OURSE_SCOPE\x10\x02\x12\r\n\tORG_SCOPE\x10\x03\x12\r\n\tALL_SCOPE\x10\x04*E\n\x08\x46ileType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0c\n\x08MARKDOWN\x10\x01\x12\x08\n\x04TEXT\x10\x02\x12\n\n\x06PYTHON\x10\x03\x12\x08\n\x04\x43ODE\x10\x04*R\n\x0c\x44ocumentType\x12\x12\n\x0eUNKOWN_CONTENT\x10\x00\x12\x0e\n\nSUPPORTING\x10\x01\x12\x0e\n\nASSIGNMENT\x10\x02\x12\x0e\n\nSUBMISSION\x10\x03\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "rag_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_SCOPETYPE"]._serialized_start = 1512
    _globals["_SCOPETYPE"]._serialized_end = 1612
    _globals["_FILETYPE"]._serialized_start = 1614
    _globals["_FILETYPE"]._serialized_end = 1683
    _globals["_DOCUMENTTYPE"]._serialized_start = 1685
    _globals["_DOCUMENTTYPE"]._serialized_end = 1767
    _globals["_DOCUMENTSOURCE"]._serialized_start = 37
    _globals["_DOCUMENTSOURCE"]._serialized_end = 193
    _globals["_SUPPORTINGDOCUMENT"]._serialized_start = 196
    _globals["_SUPPORTINGDOCUMENT"]._serialized_end = 379
    _globals["_DOCUMENTCHUNKINGSTARTED"]._serialized_start = 382
    _globals["_DOCUMENTCHUNKINGSTARTED"]._serialized_end = 544
    _globals["_DOCUMENTCHUNKS"]._serialized_start = 547
    _globals["_DOCUMENTCHUNKS"]._serialized_end = 710
    _globals["_DOCUMENTCHUNKSUMMARIZATIONSTARTED"]._serialized_start = 713
    _globals["_DOCUMENTCHUNKSUMMARIZATIONSTARTED"]._serialized_end = 852
    _globals["_CHUNKSUMMARY"]._serialized_start = 854
    _globals["_CHUNKSUMMARY"]._serialized_end = 927
    _globals["_DOCUMENTCHUNKSUMMARIES"]._serialized_start = 930
    _globals["_DOCUMENTCHUNKSUMMARIES"]._serialized_end = 1072
    _globals["_DOCUMENTPASSAGEEMBEDDINGSTARTED"]._serialized_start = 1075
    _globals["_DOCUMENTPASSAGEEMBEDDINGSTARTED"]._serialized_end = 1247
    _globals["_EMBEDDING"]._serialized_start = 1249
    _globals["_EMBEDDING"]._serialized_end = 1279
    _globals["_PASSAGEEMBEDDING"]._serialized_start = 1281
    _globals["_PASSAGEEMBEDDING"]._serialized_end = 1357
    _globals["_DOCUMENTPASSAGEEMBEDDINGS"]._serialized_start = 1360
    _globals["_DOCUMENTPASSAGEEMBEDDINGS"]._serialized_end = 1510
# @@protoc_insertion_point(module_scope)
