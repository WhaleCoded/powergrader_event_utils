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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bgrade.proto\x12\x05grade\"X\n\x0fGradeIdentifier\x12\x15\n\rsubmission_id\x18\x01 \x01(\t\x12\x15\n\rassignment_id\x18\x02 \x01(\t\x12\x17\n\x0fgrade_method_id\x18\x03 \x01(\t\"\x82\x01\n\x0eGradingStarted\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\rsubmission_id\x18\x02 \x01(\t\x12\x15\n\rassignment_id\x18\x03 \x01(\t\x12\x17\n\x0fgrade_method_id\x18\x04 \x01(\t\x12\x1d\n\x15\x63riteria_to_be_graded\x18\x05 \x03(\t\"\xe6\x01\n\rCriteriaGrade\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1c\n\x12grading_started_id\x18\x02 \x01(\tH\x00\x12\x32\n\x10grade_identifier\x18\x03 \x01(\x0b\x32\x16.grade.GradeIdentifierH\x00\x12\x1a\n\x12rubric_criteria_id\x18\x04 \x01(\t\x12\x1e\n\x04type\x18\x05 \x01(\x0e\x32\x10.grade.GradeType\x12\x12\n\x05score\x18\x06 \x01(\rH\x01\x88\x01\x01\x12\x11\n\tassesment\x18\x07 \x01(\tB\n\n\x08grade_idB\x08\n\x06_score\"c\n\x16\x43riteriaGradeEmbedding\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\rcrit_grade_id\x18\x02 \x01(\t\x12\x13\n\x0b\x65mbedder_id\x18\x03 \x01(\t\x12\x11\n\tembedding\x18\x04 \x03(\x02\"G\n\x14\x41ssessmentSimilarity\x12\n\n\x02id\x18\x01 \x01(\t\x12#\n\x1bsimmilar_criteria_grade_ids\x18\x04 \x03(\t\"\x8a\x01\n\x17StudentRequestedRegrade\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nstudent_id\x18\x02 \x01(\t\x12\x15\n\rsubmission_id\x18\x03 \x01(\t\x12\x11\n\treasoning\x18\x04 \x01(\t\x12%\n\x1d\x63riteria_grades_to_reevaluate\x18\x05 \x03(\t\"\x7f\n\x10InstructorReview\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\rsubmission_id\x18\x02 \x01(\t\x12\x15\n\rassignment_id\x18\x03 \x01(\t\x12\x15\n\rinstructor_id\x18\x04 \x01(\t\x12\x1a\n\x12\x63riteria_grade_ids\x18\x05 \x03(\t*Q\n\tGradeType\x12\x0e\n\nUNSECIFIED\x10\x00\x12\r\n\tAI_GRADED\x10\x01\x12\x14\n\x10\x46\x41\x43ULTY_ADJUSTED\x10\x02\x12\x0f\n\x0b\x41I_INFERRED\x10\x03\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grade_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GRADETYPE._serialized_start=922
  _GRADETYPE._serialized_end=1003
  _GRADEIDENTIFIER._serialized_start=22
  _GRADEIDENTIFIER._serialized_end=110
  _GRADINGSTARTED._serialized_start=113
  _GRADINGSTARTED._serialized_end=243
  _CRITERIAGRADE._serialized_start=246
  _CRITERIAGRADE._serialized_end=476
  _CRITERIAGRADEEMBEDDING._serialized_start=478
  _CRITERIAGRADEEMBEDDING._serialized_end=577
  _ASSESSMENTSIMILARITY._serialized_start=579
  _ASSESSMENTSIMILARITY._serialized_end=650
  _STUDENTREQUESTEDREGRADE._serialized_start=653
  _STUDENTREQUESTEDREGRADE._serialized_end=791
  _INSTRUCTORREVIEW._serialized_start=793
  _INSTRUCTORREVIEW._serialized_end=920
# @@protoc_insertion_point(module_scope)
