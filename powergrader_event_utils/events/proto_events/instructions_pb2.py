# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: instructions.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12instructions.proto\x12\x0cinstructions\"q\n\x1dRegisterAssignmentInstruction\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x1a\n\x12\x63ourse_public_uuid\x18\x02 \x01(\t\x12\x1f\n\x17\x61ssignment_version_uuid\x18\x03 \x01(\t\"\x88\x01\n\x1cRegisterCriterionInstruction\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x1a\n\x12\x63ourse_public_uuid\x18\x02 \x01(\t\x12\x1f\n\x17\x61ssignment_version_uuid\x18\x03 \x01(\t\x12\x16\n\x0e\x63riterion_uuid\x18\x04 \x01(\t\"n\n\x15\x41ssignmentInstruction\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x19\n\x11version_timestamp\x18\x04 \x01(\x04\"m\n\x14\x43riterionInstruction\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x14\n\x0cversion_uuid\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x19\n\x11version_timestamp\x18\x04 \x01(\x04\"\x7f\n\x15InvalidateInstruction\x12 \n\x18instruction_version_uuid\x18\x01 \x01(\t\x12&\n\x19is_assignment_instruction\x18\x02 \x01(\x08H\x00\x88\x01\x01\x42\x1c\n\x1a_is_assignment_instruction\"l\n\x0fInstructionInfo\x12,\n$assignment_instruction_version_uuids\x18\x01 \x03(\t\x12+\n#criterion_instruction_version_uuids\x18\x02 \x03(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'instructions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REGISTERASSIGNMENTINSTRUCTION']._serialized_start=36
  _globals['_REGISTERASSIGNMENTINSTRUCTION']._serialized_end=149
  _globals['_REGISTERCRITERIONINSTRUCTION']._serialized_start=152
  _globals['_REGISTERCRITERIONINSTRUCTION']._serialized_end=288
  _globals['_ASSIGNMENTINSTRUCTION']._serialized_start=290
  _globals['_ASSIGNMENTINSTRUCTION']._serialized_end=400
  _globals['_CRITERIONINSTRUCTION']._serialized_start=402
  _globals['_CRITERIONINSTRUCTION']._serialized_end=511
  _globals['_INVALIDATEINSTRUCTION']._serialized_start=513
  _globals['_INVALIDATEINSTRUCTION']._serialized_end=640
  _globals['_INSTRUCTIONINFO']._serialized_start=642
  _globals['_INSTRUCTIONINFO']._serialized_end=750
# @@protoc_insertion_point(module_scope)
