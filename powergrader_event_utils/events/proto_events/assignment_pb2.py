# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: assignment.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x61ssignment.proto\x12\nassignment\"\xb2\x01\n\nAssignment\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x1e\n\x16instructor_public_uuid\x18\x02 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x03 \x01(\t\x12\x1b\n\x13rubric_version_uuid\x18\x04 \x01(\t\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12\x19\n\x11version_timestamp\x18\x07 \x01(\x04\"\x91\x02\n\x06Rubric\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x02 \x01(\t\x12\x1e\n\x16instructor_public_uuid\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12?\n\x0frubric_criteria\x18\x05 \x03(\x0b\x32&.assignment.Rubric.RubricCriteriaEntry\x12\x19\n\x11version_timestamp\x18\x06 \x01(\x04\x1aR\n\x13RubricCriteriaEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.assignment.RubricCriterion:\x02\x38\x01\"Y\n\x0fRubricCriterion\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12*\n\x06levels\x18\x03 \x03(\x0b\x32\x1a.assignment.CriterionLevel\"C\n\x0e\x43riterionLevel\x12\x12\n\x05score\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\tB\x08\n\x06_scoreb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'assignment_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RUBRIC_RUBRICCRITERIAENTRY._options = None
  _RUBRIC_RUBRICCRITERIAENTRY._serialized_options = b'8\001'
  _ASSIGNMENT._serialized_start=33
  _ASSIGNMENT._serialized_end=211
  _RUBRIC._serialized_start=214
  _RUBRIC._serialized_end=487
  _RUBRIC_RUBRICCRITERIAENTRY._serialized_start=405
  _RUBRIC_RUBRICCRITERIAENTRY._serialized_end=487
  _RUBRICCRITERION._serialized_start=489
  _RUBRICCRITERION._serialized_end=578
  _CRITERIONLEVEL._serialized_start=580
  _CRITERIONLEVEL._serialized_end=647
# @@protoc_insertion_point(module_scope)
