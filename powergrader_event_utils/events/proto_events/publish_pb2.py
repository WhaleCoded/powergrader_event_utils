# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: publish.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpublish.proto\x12\x07publish\"a\n\x18RegisterCoursePublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x0e\n\x06lms_id\x18\x02 \x01(\t\x12 \n\x18organization_public_uuid\x18\x03 \x01(\t\"b\n\x19RegisterSectionPublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x0e\n\x06lms_id\x18\x02 \x01(\t\x12 \n\x18organization_public_uuid\x18\x03 \x01(\t\"\x94\x01\n\x1cRegisterInstructorPublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x0e\n\x06lms_id\x18\x02 \x01(\t\x12-\n\tuser_type\x18\x03 \x01(\x0e\x32\x1a.publish.LMSInstructorType\x12 \n\x18organization_public_uuid\x18\x04 \x01(\t\"b\n\x19RegisterStudentPublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x0e\n\x06lms_id\x18\x02 \x01(\t\x12 \n\x18organization_public_uuid\x18\x03 \x01(\t\"e\n\x1cRegisterAssignmentPublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x0e\n\x06lms_id\x18\x02 \x01(\t\x12 \n\x18organization_public_uuid\x18\x03 \x01(\t\"a\n\x18RegisterRubricPublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x0e\n\x06lms_id\x18\x02 \x01(\t\x12 \n\x18organization_public_uuid\x18\x03 \x01(\t\"\x88\x01\n\x1cRegisterSubmissionPublicUUID\x12\x13\n\x0bpublic_uuid\x18\x01 \x01(\t\x12\x19\n\x11lms_assignment_id\x18\x02 \x01(\t\x12\x16\n\x0elms_student_id\x18\x03 \x01(\t\x12 \n\x18organization_public_uuid\x18\x04 \x01(\t\"U\n\x0ePublishedToLMS\x12(\n version_uuid_of_published_entity\x18\x01 \x01(\t\x12\x19\n\x11publish_timestamp\x18\x02 \x01(\x04\"`\n\x13PublishedGradeToLMS\x12.\n&instructor_grade_approval_version_uuid\x18\x01 \x01(\t\x12\x19\n\x11publish_timestamp\x18\x02 \x01(\x04*9\n\x11LMSInstructorType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x06\n\x02TA\x10\x01\x12\x0b\n\x07\x46\x41\x43ULTY\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'publish_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LMSINSTRUCTORTYPE._serialized_start=1002
  _LMSINSTRUCTORTYPE._serialized_end=1059
  _REGISTERCOURSEPUBLICUUID._serialized_start=26
  _REGISTERCOURSEPUBLICUUID._serialized_end=123
  _REGISTERSECTIONPUBLICUUID._serialized_start=125
  _REGISTERSECTIONPUBLICUUID._serialized_end=223
  _REGISTERINSTRUCTORPUBLICUUID._serialized_start=226
  _REGISTERINSTRUCTORPUBLICUUID._serialized_end=374
  _REGISTERSTUDENTPUBLICUUID._serialized_start=376
  _REGISTERSTUDENTPUBLICUUID._serialized_end=474
  _REGISTERASSIGNMENTPUBLICUUID._serialized_start=476
  _REGISTERASSIGNMENTPUBLICUUID._serialized_end=577
  _REGISTERRUBRICPUBLICUUID._serialized_start=579
  _REGISTERRUBRICPUBLICUUID._serialized_end=676
  _REGISTERSUBMISSIONPUBLICUUID._serialized_start=679
  _REGISTERSUBMISSIONPUBLICUUID._serialized_end=815
  _PUBLISHEDTOLMS._serialized_start=817
  _PUBLISHEDTOLMS._serialized_end=902
  _PUBLISHEDGRADETOLMS._serialized_start=904
  _PUBLISHEDGRADETOLMS._serialized_end=1000
# @@protoc_insertion_point(module_scope)
