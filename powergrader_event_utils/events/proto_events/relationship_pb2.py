# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: relationship.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12relationship.proto\x12\x0crelationship\"?\n\x12RegisterPublicUuid\x12\x14\n\x0cprivate_uuid\x18\x01 \x01(\t\x12\x13\n\x0bpublic_uuid\x18\x02 \x01(\t\"A\n\x16\x41ssignmentAddedToClass\x12\x15\n\rassignment_id\x18\x01 \x01(\t\x12\x10\n\x08\x63lass_id\x18\x02 \x01(\t\"E\n\x1a\x41ssignmentRemovedFromClass\x12\x15\n\rassignment_id\x18\x01 \x01(\t\x12\x10\n\x08\x63lass_id\x18\x02 \x01(\t\";\n\x13StudentAddedToClass\x12\x12\n\nstudent_id\x18\x01 \x01(\t\x12\x10\n\x08\x63lass_id\x18\x02 \x01(\t\"?\n\x17StudentRemovedFromClass\x12\x12\n\nstudent_id\x18\x01 \x01(\t\x12\x10\n\x08\x63lass_id\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'relationship_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTERPUBLICUUID._serialized_start=36
  _REGISTERPUBLICUUID._serialized_end=99
  _ASSIGNMENTADDEDTOCLASS._serialized_start=101
  _ASSIGNMENTADDEDTOCLASS._serialized_end=166
  _ASSIGNMENTREMOVEDFROMCLASS._serialized_start=168
  _ASSIGNMENTREMOVEDFROMCLASS._serialized_end=237
  _STUDENTADDEDTOCLASS._serialized_start=239
  _STUDENTADDEDTOCLASS._serialized_end=298
  _STUDENTREMOVEDFROMCLASS._serialized_start=300
  _STUDENTREMOVEDFROMCLASS._serialized_end=363
# @@protoc_insertion_point(module_scope)
