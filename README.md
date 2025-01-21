[![DOI](https://zenodo.org/badge/919743668.svg)](https://doi.org/10.5281/zenodo.14708731)


# Thesis Supplementary Materials: *Large Language Models in Software Engineering: A Critical Review of Evaluation Strategies*

This repository contains the supplementary materials for the Master’s thesis titled *Large Language Models in Software Engineering: A Critical Review of Evaluation Strategies*, submitted to the Freie Universität Berlin, Department of Computer Science, Software Engineering Group. The thesis was authored by Ali Bektas and supervised by Prof. Dr. Lutz Prechelt, with second supervision by Prof. Dr. Michael Felderer (DLR), and mentoring by Carina Haupt (DLR).

The thesis investigates evaluation strategies employed in research on Large Language Models (LLMs) for Software Engineering (SE), focusing on their reliability and relevance. Using a structured six-phase approach, the thesis critically reviews 41 papers, highlighting opportunities for improvement and actionable recommendations to enhance evaluation practices.

---


## Repository Contents

### 1. **Thesis Document**
The complete thesis is available as a PDF:
- [Master Thesis PDF](https://github.com/Alioio/thesis_llms4se_review/blob/main/master_thesis_large_language_models_se_critical_review_evaluation_strategies.pdf)

---

### 2. **Data**
The `data` folder contains review notes and structured information used in the thesis, including:
- Reliability and relevance scores for evaluated papers.
- Research focus categories assigned to papers.
- Task objective group categorizations.
  
**Review Data** [Data Folder](https://github.com/Alioio/thesis_llms4se_review/tree/main/thesis_research_focus_categorization/data)

---

### 3. **Source Code**
The `src` folder contains the source code used to classify research focus categories and process data for the review. This includes:

- **Research Focus Categorization Code:**
  - Implements tagging logic for assining the research focus category using OpenAI's API and LangChain library.
  - [Tag Extraction Code](https://github.com/Alioio/thesis_llms4se_review/blob/main/thesis_research_focus_categorization/src/tag_extraction/tag_extractor.py)

- **Tagging Schema Definition:**
  - Provides a structured schema to classify papers into research focus categories.
  - [Tagging Schema](https://github.com/Alioio/thesis_llms4se_review/blob/main/thesis_research_focus_categorization/src/tag_extraction/tagging_schema.py)

-------------------------------------------------------------------------------

@software{bektas_2025_14708732,
  author       = {Ali Bektas},
  title        = {alioio/thesis\_llms4se\_review: Categorization Code and Review Data (21.01.2025)},
  month        = jan,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {submitting\_thesis},
  doi          = {10.5281/zenodo.14708732},
  url          = {https://doi.org/10.5281/zenodo.14708732}
}

----------------------------------------------------------------------

## Contact

For any questions, feedback, or collaboration opportunities, please reach out to:

- **Ali Bektas** (Author)  
  Email: [alib10@zedat.fu-berlin.de](mailto:alib10@zedat.fu-berlin.de)  
  GitHub: [Alioio](https://github.com/Alioio)

## License

This repository is distributed under the **MIT License**. You are free to use, modify, and distribute this work, provided that proper credit is given to the author. For more details, see the [LICENSE](LICENSE) file included in this repository.


