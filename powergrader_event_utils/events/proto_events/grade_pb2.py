# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grade.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bgrade.proto\x12\x05grade\"\x80\x01\n\x19\x41ICriterionGradingStarted\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x16\n\x0e\x63riterion_uuid\x18\x02 \x01(\t\x12\x1f\n\x17submission_version_uuid\x18\x03 \x01(\t\x12\x14\n\x0ctime_started\x18\x04 \x01(\x04\"X\n\rGradingMethod\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t\x12\x13\n\x0bmethod_name\x18\x03 \x01(\t\x12\x10\n\x08git_hash\x18\x04 \x01(\t\"9\n\x05Grade\x12\x12\n\x05score\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x12\n\nassessment\x18\x02 \x01(\tB\x08\n\x06_score\"\x89\x01\n\x10\x41ICriterionGrade\x12$\n\x1cgrading_started_version_uuid\x18\x01 \x01(\t\x12\x1b\n\x13grading_method_uuid\x18\x04 \x01(\t\x12\x1b\n\x05grade\x18\x05 \x01(\x0b\x32\x0c.grade.Grade\x12\x15\n\rtime_finished\x18\x06 \x01(\x04\"\xf7\x01\n\x18\x41IInferredCriterionGrade\x12$\n\x1cgrading_started_version_uuid\x18\x01 \x01(\t\x12\x1b\n\x13grading_method_uuid\x18\x04 \x01(\t\x12-\n%previous_criterion_grade_version_uuid\x18\x05 \x01(\t\x12\x35\n-faculty_override_criterion_grade_version_uuid\x18\x06 \x01(\t\x12\x1b\n\x05grade\x18\x07 \x01(\x0b\x32\x0c.grade.Grade\x12\x15\n\rtime_finished\x18\x08 \x01(\x04\"\xa6\x01\n\x18InstructorCriterionGrade\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x16\n\x0e\x63riterion_uuid\x18\x02 \x01(\t\x12\x1f\n\x17submission_version_uuid\x18\x03 \x01(\t\x12\x1e\n\x16instructor_public_uuid\x18\x04 \x01(\t\x12\x1b\n\x05grade\x18\x05 \x01(\x0b\x32\x0c.grade.Grade\"\xdd\x01\n InstructorOverrideCriterionGrade\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x16\n\x0e\x63riterion_uuid\x18\x02 \x01(\t\x12\x1f\n\x17submission_version_uuid\x18\x03 \x01(\t\x12-\n%previous_criterion_grade_version_uuid\x18\x04 \x01(\t\x12\x1e\n\x16instructor_public_uuid\x18\x05 \x01(\t\x12\x1b\n\x05grade\x18\x06 \x01(\x0b\x32\x0c.grade.Grade\"\x7f\n\x17\x43riterionGradeEmbedding\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12$\n\x1c\x63riterion_grade_version_uuid\x18\x02 \x01(\t\x12\x15\n\rembedder_uuid\x18\x03 \x01(\t\x12\x11\n\tembedding\x18\x04 \x03(\x02\"\xbc\x01\n!InstructorSubmissionGradeApproval\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x1f\n\x17submission_version_uuid\x18\x02 \x01(\t\x12\x1e\n\x16instructor_public_uuid\x18\x03 \x01(\t\x12%\n\x1d\x63riterion_grade_version_uuids\x18\x04 \x03(\t\x12\x19\n\x11version_timestamp\x18\x05 \x01(\x04\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grade_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AICRITERIONGRADINGSTARTED._serialized_start=23
  _AICRITERIONGRADINGSTARTED._serialized_end=151
  _GRADINGMETHOD._serialized_start=153
  _GRADINGMETHOD._serialized_end=241
  _GRADE._serialized_start=243
  _GRADE._serialized_end=300
  _AICRITERIONGRADE._serialized_start=303
  _AICRITERIONGRADE._serialized_end=440
  _AIINFERREDCRITERIONGRADE._serialized_start=443
  _AIINFERREDCRITERIONGRADE._serialized_end=690
  _INSTRUCTORCRITERIONGRADE._serialized_start=693
  _INSTRUCTORCRITERIONGRADE._serialized_end=859
  _INSTRUCTOROVERRIDECRITERIONGRADE._serialized_start=862
  _INSTRUCTOROVERRIDECRITERIONGRADE._serialized_end=1083
  _CRITERIONGRADEEMBEDDING._serialized_start=1085
  _CRITERIONGRADEEMBEDDING._serialized_end=1212
  _INSTRUCTORSUBMISSIONGRADEAPPROVAL._serialized_start=1215
  _INSTRUCTORSUBMISSIONGRADEAPPROVAL._serialized_end=1403
# @@protoc_insertion_point(module_scope)
