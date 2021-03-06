from PDS_Extractors.Reporting.ReportType import ReportType


class ReportGroupings:
    parts_reports = [
        ReportType.EPUSplit,
        ReportType.FamilyParts,
        ReportType.FamilyExclusiveParts,
        ReportType.CostAnalysisComponentsAndParts,
        ReportType.TechDocDeltaComponentsAndParts,
        ReportType.TechDocInvertedSequenceComponentsAndParts,
        ReportType.TechDocNoConclusionComponentsAndParts
    ]

    cost_analysis_reports = [
        ReportType.CostAnalysisComponents,
        ReportType.CostAnalysisComponentsAndParts
    ]

    tech_doc_reports = [
        ReportType.TechDocDeltaComponents,
        ReportType.TechDocDeltaComponentsAndParts,
        ReportType.TechDocInvertedSequenceComponents,
        ReportType.TechDocInvertedSequenceComponentsAndParts,
        ReportType.TechDocNoConclusionComponents,
        ReportType.TechDocNoConclusionComponentsAndParts
    ]

    tech_doc_delta_reports = [
        ReportType.TechDocDeltaComponents,
        ReportType.TechDocDeltaComponentsAndParts
    ]

    tech_doc_inverted_sequence_reports = [
        ReportType.TechDocInvertedSequenceComponents,
        ReportType.TechDocInvertedSequenceComponentsAndParts
    ]

    tech_doc_no_conclusion_reports = [
        ReportType.TechDocNoConclusionComponents,
        ReportType.TechDocNoConclusionComponentsAndParts
    ]

    extract_saa_reports = [
        ReportType.ExtractSAAFromAGRMZ_SBC,
        ReportType.ExtractSAAFromAGRMZ_JDF
    ]

    extract_optionals_reports = [
        ReportType.ExtractOptionalsPartsFrom3CA_SBC,
        ReportType.ExtractOptionalsPartsFrom3CA_JDF
    ]

    extract_saa_and_parts_from_bm = [
        ReportType.ExtractSAAandPartsfromBM_SBC,
        ReportType.ExtractSAAandPartsfromBM_JDF
    ]
