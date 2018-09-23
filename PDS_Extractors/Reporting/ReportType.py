from enum import Enum


class ReportType(Enum):
    CostAnalysisComponents = "Analise de Custo - Componentes"
    CostAnalysisComponentsAndParts = "Analise de Custo - Componentes e Partes"
    EPUSplit = "EPU Split"
    TechDocDeltaComponents = "TechDoc - Delta Tecnico - Componentes"
    TechDocDeltaComponentsAndParts = "TechDoc - Delta Tecnico - Componentes e Pecas"
    TechDocInvertedSequenceComponents = "Tech Doc - Inversoes de Sequencia - Componentes"
    TechDocInvertedSequenceComponentsAndParts = "Tech Doc - Inversoes de Sequencia - Componentes e Partes"
    TechDocNoConclusionComponents = "TechDoc - Nao Conclusivos - Componentes"
    TechDocNoConclusionComponentsAndParts = "TechDoc - Nao Conclusivos - Componentes e Partes"
