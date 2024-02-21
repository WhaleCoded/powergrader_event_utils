# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: retry.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import assignment_pb2 as assignment__pb2
import course_pb2 as course__pb2
import grade_pb2 as grade__pb2
import publish_pb2 as publish__pb2
import relationship_pb2 as relationship__pb2
import submission_pb2 as submission__pb2
import user_pb2 as user__pb2
import embedding_pb2 as embedding__pb2
import artifacts_pb2 as artifacts__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bretry.proto\x12\revent_wrapper\x1a\x10\x61ssignment.proto\x1a\x0c\x63ourse.proto\x1a\x0bgrade.proto\x1a\rpublish.proto\x1a\x12relationship.proto\x1a\x10submission.proto\x1a\nuser.proto\x1a\x0f\x65mbedding.proto\x1a\x0f\x61rtifacts.proto\"\xae\x15\n\x05Retry\x12\x14\n\x0cretry_number\x18\x01 \x01(\r\x12\x14\n\x0cretry_reason\x18\x02 \x01(\t\x12<\n\x13\x61ssignment_artifact\x18\x03 \x01(\x0b\x32\x1d.artifacts.AssignmentArtifactH\x00\x12<\n\x13submission_artifact\x18\x04 \x01(\x0b\x32\x1d.artifacts.SubmissionArtifactH\x00\x12:\n\x12\x63riterion_artifact\x18\x05 \x01(\x0b\x32\x1c.artifacts.CriterionArtifactH\x00\x12\x45\n\x18\x63riterion_grade_artifact\x18\x06 \x01(\x0b\x32!.artifacts.CriterionGradeArtifactH\x00\x12.\n\x0c\x61rtifact_log\x18\x07 \x01(\x0b\x32\x16.artifacts.ArtifactLogH\x00\x12,\n\nassignment\x18\x08 \x01(\x0b\x32\x16.assignment.AssignmentH\x00\x12$\n\x06rubric\x18\t \x01(\x0b\x32\x12.assignment.RubricH\x00\x12 \n\x06\x63ourse\x18\n \x01(\x0b\x32\x0e.course.CourseH\x00\x12\"\n\x07section\x18\x0b \x01(\x0b\x32\x0f.course.SectionH\x00\x12,\n\x0corganization\x18\x0c \x01(\x0b\x32\x14.course.OrganizationH\x00\x12>\n\x14\x61ssignment_embedding\x18\r \x01(\x0b\x32\x1e.embedding.AssignmentEmbeddingH\x00\x12<\n\x13\x63riterion_embedding\x18\x0e \x01(\x0b\x32\x1d.embedding.CriterionEmbeddingH\x00\x12G\n\x19\x63riterion_grade_embedding\x18\x0f \x01(\x0b\x32\".embedding.CriterionGradeEmbeddingH\x00\x12>\n\x14submission_embedding\x18\x10 \x01(\x0b\x32\x1e.embedding.SubmissionEmbeddingH\x00\x12:\n\x12\x61rtifact_embedding\x18\x11 \x01(\x0b\x32\x1c.embedding.ArtifactEmbeddingH\x00\x12H\n\x1c\x61i_criterion_grading_started\x18\x12 \x01(\x0b\x32 .grade.AICriterionGradingStartedH\x00\x12.\n\x0egrading_method\x18\x13 \x01(\x0b\x32\x14.grade.GradingMethodH\x00\x12\x35\n\x12\x61i_criterion_grade\x18\x14 \x01(\x0b\x32\x17.grade.AICriterionGradeH\x00\x12\x46\n\x1b\x61i_inferred_criterion_grade\x18\x15 \x01(\x0b\x32\x1f.grade.AIInferredCriterionGradeH\x00\x12\x45\n\x1ainstructor_criterion_grade\x18\x16 \x01(\x0b\x32\x1f.grade.InstructorCriterionGradeH\x00\x12V\n#instructor_override_criterion_grade\x18\x17 \x01(\x0b\x32\'.grade.InstructorOverrideCriterionGradeH\x00\x12X\n$instructor_submission_grade_approval\x18\x18 \x01(\x0b\x32(.grade.InstructorSubmissionGradeApprovalH\x00\x12H\n\x1bregister_course_public_uuid\x18\x19 \x01(\x0b\x32!.publish.RegisterCoursePublicUUIDH\x00\x12J\n\x1cregister_section_public_uuid\x18\x1a \x01(\x0b\x32\".publish.RegisterSectionPublicUUIDH\x00\x12P\n\x1fregister_instructor_public_uuid\x18\x1b \x01(\x0b\x32%.publish.RegisterInstructorPublicUUIDH\x00\x12J\n\x1cregister_student_public_uuid\x18\x1c \x01(\x0b\x32\".publish.RegisterStudentPublicUUIDH\x00\x12P\n\x1fregister_assignment_public_uuid\x18\x1d \x01(\x0b\x32%.publish.RegisterAssignmentPublicUUIDH\x00\x12H\n\x1bregister_rubric_public_uuid\x18\x1e \x01(\x0b\x32!.publish.RegisterRubricPublicUUIDH\x00\x12P\n\x1fregister_submission_public_uuid\x18\x1f \x01(\x0b\x32%.publish.RegisterSubmissionPublicUUIDH\x00\x12\x33\n\x10published_to_lms\x18  \x01(\x0b\x32\x17.publish.PublishedToLMSH\x00\x12>\n\x16published_grade_to_lms\x18! \x01(\x0b\x32\x1c.publish.PublishedGradeToLMSH\x00\x12K\n\x1a\x61ssignment_added_to_course\x18\" \x01(\x0b\x32%.relationship.AssignmentAddedToCourseH\x00\x12S\n\x1e\x61ssignment_removed_from_course\x18# \x01(\x0b\x32).relationship.AssignmentRemovedFromCourseH\x00\x12G\n\x18student_added_to_section\x18$ \x01(\x0b\x32#.relationship.StudentAddedToSectionH\x00\x12O\n\x1cstudent_removed_from_section\x18% \x01(\x0b\x32\'.relationship.StudentRemovedFromSectionH\x00\x12K\n\x1ainstructor_added_to_course\x18& \x01(\x0b\x32%.relationship.InstructorAddedToCourseH\x00\x12S\n\x1einstructor_removed_from_course\x18\' \x01(\x0b\x32).relationship.InstructorRemovedFromCourseH\x00\x12,\n\nsubmission\x18( \x01(\x0b\x32\x16.submission.SubmissionH\x00\x12@\n\x15submission_file_group\x18) \x01(\x0b\x32\x1f.submission.SubmissionFileGroupH\x00\x12 \n\x07student\x18* \x01(\x0b\x32\r.user.StudentH\x00\x12&\n\ninstructor\x18+ \x01(\x0b\x32\x10.user.InstructorH\x00\x12\x15\n\rinstance_name\x18, \x01(\tB\x07\n\x05\x65vent\"\xa3\x15\n\nDeadLetter\x12\x1a\n\x12\x64\x65\x61\x64_letter_reason\x18\x01 \x01(\t\x12\x15\n\rinstance_name\x18\x02 \x01(\t\x12<\n\x13\x61ssignment_artifact\x18\x03 \x01(\x0b\x32\x1d.artifacts.AssignmentArtifactH\x00\x12<\n\x13submission_artifact\x18\x04 \x01(\x0b\x32\x1d.artifacts.SubmissionArtifactH\x00\x12:\n\x12\x63riterion_artifact\x18\x05 \x01(\x0b\x32\x1c.artifacts.CriterionArtifactH\x00\x12\x45\n\x18\x63riterion_grade_artifact\x18\x06 \x01(\x0b\x32!.artifacts.CriterionGradeArtifactH\x00\x12.\n\x0c\x61rtifact_log\x18\x07 \x01(\x0b\x32\x16.artifacts.ArtifactLogH\x00\x12,\n\nassignment\x18\x08 \x01(\x0b\x32\x16.assignment.AssignmentH\x00\x12$\n\x06rubric\x18\t \x01(\x0b\x32\x12.assignment.RubricH\x00\x12 \n\x06\x63ourse\x18\n \x01(\x0b\x32\x0e.course.CourseH\x00\x12\"\n\x07section\x18\x0b \x01(\x0b\x32\x0f.course.SectionH\x00\x12,\n\x0corganization\x18\x0c \x01(\x0b\x32\x14.course.OrganizationH\x00\x12>\n\x14\x61ssignment_embedding\x18\r \x01(\x0b\x32\x1e.embedding.AssignmentEmbeddingH\x00\x12<\n\x13\x63riterion_embedding\x18\x0e \x01(\x0b\x32\x1d.embedding.CriterionEmbeddingH\x00\x12G\n\x19\x63riterion_grade_embedding\x18\x0f \x01(\x0b\x32\".embedding.CriterionGradeEmbeddingH\x00\x12>\n\x14submission_embedding\x18\x10 \x01(\x0b\x32\x1e.embedding.SubmissionEmbeddingH\x00\x12:\n\x12\x61rtifact_embedding\x18\x11 \x01(\x0b\x32\x1c.embedding.ArtifactEmbeddingH\x00\x12H\n\x1c\x61i_criterion_grading_started\x18\x12 \x01(\x0b\x32 .grade.AICriterionGradingStartedH\x00\x12.\n\x0egrading_method\x18\x13 \x01(\x0b\x32\x14.grade.GradingMethodH\x00\x12\x35\n\x12\x61i_criterion_grade\x18\x14 \x01(\x0b\x32\x17.grade.AICriterionGradeH\x00\x12\x46\n\x1b\x61i_inferred_criterion_grade\x18\x15 \x01(\x0b\x32\x1f.grade.AIInferredCriterionGradeH\x00\x12\x45\n\x1ainstructor_criterion_grade\x18\x16 \x01(\x0b\x32\x1f.grade.InstructorCriterionGradeH\x00\x12V\n#instructor_override_criterion_grade\x18\x17 \x01(\x0b\x32\'.grade.InstructorOverrideCriterionGradeH\x00\x12X\n$instructor_submission_grade_approval\x18\x18 \x01(\x0b\x32(.grade.InstructorSubmissionGradeApprovalH\x00\x12H\n\x1bregister_course_public_uuid\x18\x19 \x01(\x0b\x32!.publish.RegisterCoursePublicUUIDH\x00\x12J\n\x1cregister_section_public_uuid\x18\x1a \x01(\x0b\x32\".publish.RegisterSectionPublicUUIDH\x00\x12P\n\x1fregister_instructor_public_uuid\x18\x1b \x01(\x0b\x32%.publish.RegisterInstructorPublicUUIDH\x00\x12J\n\x1cregister_student_public_uuid\x18\x1c \x01(\x0b\x32\".publish.RegisterStudentPublicUUIDH\x00\x12P\n\x1fregister_assignment_public_uuid\x18\x1d \x01(\x0b\x32%.publish.RegisterAssignmentPublicUUIDH\x00\x12H\n\x1bregister_rubric_public_uuid\x18\x1e \x01(\x0b\x32!.publish.RegisterRubricPublicUUIDH\x00\x12P\n\x1fregister_submission_public_uuid\x18\x1f \x01(\x0b\x32%.publish.RegisterSubmissionPublicUUIDH\x00\x12\x33\n\x10published_to_lms\x18  \x01(\x0b\x32\x17.publish.PublishedToLMSH\x00\x12>\n\x16published_grade_to_lms\x18! \x01(\x0b\x32\x1c.publish.PublishedGradeToLMSH\x00\x12K\n\x1a\x61ssignment_added_to_course\x18\" \x01(\x0b\x32%.relationship.AssignmentAddedToCourseH\x00\x12S\n\x1e\x61ssignment_removed_from_course\x18# \x01(\x0b\x32).relationship.AssignmentRemovedFromCourseH\x00\x12G\n\x18student_added_to_section\x18$ \x01(\x0b\x32#.relationship.StudentAddedToSectionH\x00\x12O\n\x1cstudent_removed_from_section\x18% \x01(\x0b\x32\'.relationship.StudentRemovedFromSectionH\x00\x12K\n\x1ainstructor_added_to_course\x18& \x01(\x0b\x32%.relationship.InstructorAddedToCourseH\x00\x12S\n\x1einstructor_removed_from_course\x18\' \x01(\x0b\x32).relationship.InstructorRemovedFromCourseH\x00\x12,\n\nsubmission\x18( \x01(\x0b\x32\x16.submission.SubmissionH\x00\x12@\n\x15submission_file_group\x18) \x01(\x0b\x32\x1f.submission.SubmissionFileGroupH\x00\x12 \n\x07student\x18* \x01(\x0b\x32\r.user.StudentH\x00\x12&\n\ninstructor\x18+ \x01(\x0b\x32\x10.user.InstructorH\x00\x42\x07\n\x05\x65ventb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'retry_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RETRY']._serialized_start=175
  _globals['_RETRY']._serialized_end=2909
  _globals['_DEADLETTER']._serialized_start=2912
  _globals['_DEADLETTER']._serialized_end=5635
# @@protoc_insertion_point(module_scope)
