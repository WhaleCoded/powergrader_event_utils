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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bgrade.proto\x12\x05grade\"~\n\x18\x41ICriteriaGradingStarted\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x15\n\rcriteria_uuid\x18\x02 \x01(\t\x12\x1f\n\x17submission_version_uuid\x18\x03 \x01(\t\x12\x14\n\x0ctime_started\x18\x04 \x01(\x04\"X\n\rGradingMethod\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t\x12\x13\n\x0bmethod_name\x18\x03 \x01(\t\x12\x10\n\x08git_hash\x18\x04 \x01(\t\"9\n\x05Grade\x12\x12\n\x05score\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x12\n\nassessment\x18\x02 \x01(\tB\x08\n\x06_score\"\xbe\x01\n\x0f\x41ICriteriaGrade\x12$\n\x1cgrading_started_version_uuid\x18\x01 \x01(\t\x12\x15\n\rcriteria_uuid\x18\x02 \x01(\t\x12\x1f\n\x17sumbission_version_uuid\x18\x03 \x01(\t\x12\x19\n\x11grade_method_uuid\x18\x04 \x01(\t\x12\x1b\n\x05grade\x18\x05 \x01(\x0b\x32\x0c.grade.Grade\x12\x15\n\rtime_finished\x18\x06 \x01(\x04\"\xaa\x02\n\x17\x41IInferredCriteriaGrade\x12$\n\x1cgrading_started_version_uuid\x18\x01 \x01(\t\x12\x15\n\rcriteria_uuid\x18\x02 \x01(\t\x12\x1f\n\x17sumbission_version_uuid\x18\x03 \x01(\t\x12\x19\n\x11grade_method_uuid\x18\x04 \x01(\t\x12,\n$previous_criteria_grade_version_uuid\x18\x05 \x01(\t\x12\x34\n,faculty_override_criteria_grade_version_uuid\x18\x06 \x01(\t\x12\x1b\n\x05grade\x18\x07 \x01(\x0b\x32\x0c.grade.Grade\x12\x15\n\rtime_finished\x18\x08 \x01(\x04\"\x81\x01\n\x14\x46\x61\x63ultyCriteriaGrade\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x15\n\rcriteria_uuid\x18\x02 \x01(\t\x12\x1f\n\x17sumbission_version_uuid\x18\x03 \x01(\t\x12\x1b\n\x05grade\x18\x04 \x01(\x0b\x32\x0c.grade.Grade\"\xb7\x01\n\x1c\x46\x61\x63ultyOverrideCriteriaGrade\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x15\n\rcriteria_uuid\x18\x02 \x01(\t\x12\x1f\n\x17sumbission_version_uuid\x18\x03 \x01(\t\x12,\n$previous_criteria_grade_version_uuid\x18\x04 \x01(\t\x12\x1b\n\x05grade\x18\x05 \x01(\x0b\x32\x0c.grade.Grade\"}\n\x16\x43riteriaGradeEmbedding\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12#\n\x1b\x63riteria_grade_version_uuid\x18\x02 \x01(\t\x12\x15\n\rembedder_uuid\x18\x03 \x01(\t\x12\x11\n\tembedding\x18\x04 \x03(\x02\"\xbb\x01\n!InstructorSubmissionGradeApproval\x12\x14\n\x0cversion_uuid\x18\x01 \x01(\t\x12\x1f\n\x17submission_version_uuid\x18\x02 \x01(\t\x12\x1e\n\x16instructor_public_uuid\x18\x03 \x01(\t\x12$\n\x1c\x63riteria_grade_version_uuids\x18\x04 \x03(\t\x12\x19\n\x11version_timestamp\x18\x05 \x01(\x04\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grade_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AICRITERIAGRADINGSTARTED._serialized_start=22
  _AICRITERIAGRADINGSTARTED._serialized_end=148
  _GRADINGMETHOD._serialized_start=150
  _GRADINGMETHOD._serialized_end=238
  _GRADE._serialized_start=240
  _GRADE._serialized_end=297
  _AICRITERIAGRADE._serialized_start=300
  _AICRITERIAGRADE._serialized_end=490
  _AIINFERREDCRITERIAGRADE._serialized_start=493
  _AIINFERREDCRITERIAGRADE._serialized_end=791
  _FACULTYCRITERIAGRADE._serialized_start=794
  _FACULTYCRITERIAGRADE._serialized_end=923
  _FACULTYOVERRIDECRITERIAGRADE._serialized_start=926
  _FACULTYOVERRIDECRITERIAGRADE._serialized_end=1109
  _CRITERIAGRADEEMBEDDING._serialized_start=1111
  _CRITERIAGRADEEMBEDDING._serialized_end=1236
  _INSTRUCTORSUBMISSIONGRADEAPPROVAL._serialized_start=1239
  _INSTRUCTORSUBMISSIONGRADEAPPROVAL._serialized_end=1426
# @@protoc_insertion_point(module_scope)
