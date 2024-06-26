import time
from uuid import uuid4

from powergrader_event_utils.events.rag import *


def create_all_rag_events():
    doc_source_event = DocumentSourceEvent("python std", None, ScopeType.ALL_SCOPE)
    doc_event = DocumentEvent(
        doc_source_event.public_uuid,
        "test.py",
        FileType.PYTHON,
        "print('hello world')\n",
    )
    rag_div_started = RAGDivisionStartedEvent(
        doc_event.version_uuid, "tanners best", ContentType.DOCUMENT
    )
    python_sec = PythonClass("class doThing:\n    def __init__(self):\n        pass\n")
    python_c = PythonCodePassage("def doThing():\n    pass\n", python_sec.uuid)
    assert isinstance(python_sec, Section)
    assert isinstance(python_c, Passage)

    doc_divided = DividedDocumentEvent(
        rag_div_started.uuid, [RAGDivision(python_sec), RAGDivision(python_c)]
    )
    for rag_div in doc_divided.divisions:
        print(f"RagDiv types: {type(rag_div)},{type(rag_div.division)}")
        assert isinstance(rag_div, RAGDivision)
        assert isinstance(rag_div.division, Section) or isinstance(
            rag_div.division, Passage
        )
        assert isinstance(rag_div.division, PythonClass) or isinstance(
            rag_div.division, PythonCodePassage
        )

    doc_sum_started = DocumentSummarizationStartedEvent(
        doc_divided.rag_division_started_uuid, "tanners best summary"
    )
    div_sum = DivisionSummary(python_sec.uuid, "This is about doing nothing")
    sum_doc_event = SummarizedDocumentEvent(doc_sum_started.uuid, [div_sum])

    doc_embed_started = DocumentEmbeddingStartedEvent(
        doc_divided.rag_division_started_uuid, "tanners best embedding"
    )
    embed = Embedding([0.0 for _ in range(100)])
    pass_embed = PassageEmbedding(python_c.uuid, [embed])
    embed_doc_event = EmbeddedDocumentEvent(doc_embed_started.uuid, [pass_embed])

    reg_assign_inst = RegisterAssignmentInstructionEvent("DNE", "DNE")
    reg_crit_inst = RegisterCriterionInstructionEvent("DNE", "DNE", "DNE")
    assign_inst = AssignmentInstructionEvent(
        "This should never be done", reg_assign_inst.public_uuid
    )
    crit_inst = CriterionInstructionEvent(
        "This should never be done", reg_crit_inst.public_uuid
    )
    invalid_inst = InvalidateInstructionEvent(False, crit_inst.version_uuid)

    root_node = FlowNode("")
    child_1 = FlowNode("thing 1", root_node.uuid)
    child_2 = FlowNode("thing 2", root_node.uuid)
    flow_log = FlowLogEvent(
        "main flow log", "ai_grading_started_id", [root_node, child_1, child_2]
    )
    assert isinstance(flow_log, FlowLogEvent)
    assert len(flow_log.nodes) == 3


def create_and_send_rag_events() -> List[ProtoPowerGraderEvent]:
    events_to_send = []

    doc_source_event = DocumentSourceEvent(name="temp", scope_type=ScopeType.ORG_SCOPE)
    events_to_send.append(doc_source_event)
    time.sleep(0.1)
    doc_source_v_2 = DocumentSourceEvent(
        name="python std",
        scope_type=ScopeType.ALL_SCOPE,
        public_uuid=doc_source_event.public_uuid,
    )
    events_to_send.append(doc_source_v_2)

    doc_event = DocumentEvent(
        doc_source_event.public_uuid,
        "test.py",
        FileType.PYTHON,
        "print('hello world')\n",
    )
    events_to_send.append(doc_event)

    rag_div_started = RAGDivisionStartedEvent(
        doc_event.version_uuid, "tanners best", ContentType.DOCUMENT
    )
    events_to_send.append(rag_div_started)

    python_sec = PythonClass("class doThing:\n    def __init__(self):\n        pass\n")
    python_c = PythonCodePassage("def doThing():\n    pass\n", python_sec.uuid)
    assert isinstance(python_sec, Section)
    assert isinstance(python_c, Passage)

    doc_divided = DividedDocumentEvent(
        rag_div_started.uuid, [RAGDivision(python_sec), RAGDivision(python_c)]
    )
    events_to_send.append(doc_divided)

    summ_started = DocumentSummarizationStartedEvent(
        doc_divided.rag_division_started_uuid, "tanners best summary"
    )
    events_to_send.append(summ_started)

    div_sum = DivisionSummary(python_sec.uuid, "This is about doing nothing")
    sum_doc = SummarizedDocumentEvent(doc_divided.rag_division_started_uuid, [div_sum])
    events_to_send.append(sum_doc)

    embed_started = DocumentEmbeddingStartedEvent(
        doc_divided.rag_division_started_uuid, "tanners best embedding"
    )
    events_to_send.append(embed_started)

    embed = Embedding([0.0 for _ in range(100)])

    pass_embed = PassageEmbedding(python_c.uuid, [embed])
    embed_doc = EmbeddedDocumentEvent(embed_started.uuid, [pass_embed])
    events_to_send.append(embed_doc)

    reg_assign_inst = RegisterAssignmentInstructionEvent(str(uuid4()), str(uuid4()))
    events_to_send.append(reg_assign_inst)

    reg_crit_inst = RegisterCriterionInstructionEvent(
        str(uuid4()), str(uuid4()), str(uuid4())
    )
    events_to_send.append(reg_crit_inst)

    assign_inst = AssignmentInstructionEvent(
        "do the ting good", reg_assign_inst.public_uuid
    )
    events_to_send.append(assign_inst)

    crit_inst = CriterionInstructionEvent("do the ting good", reg_crit_inst.public_uuid)
    events_to_send.append(crit_inst)

    invalid_inst = InvalidateInstructionEvent(False, str(uuid4()))
    events_to_send.append(invalid_inst)

    root_node = FlowNode("root")
    child_1 = FlowNode("child 1", root_node.uuid)

    flow_log = FlowLogEvent("main flow log", str(uuid4()), [root_node, child_1])
    events_to_send.append(flow_log)

    return events_to_send
