# IMAS - Integrated Medical Agentic System
_Access the paper and technical details [here](https://arxiv.org/abs/2410.12868) via [arXiv](https://arxiv.org/)_
## Introduction
IMAS is an advanced agentic medical assistant system designed to enhance healthcare delivery in rural areas, especially where experienced medical professionals are scarce. Leveraging fine-tuned healthcare domain-adapted Large Language Models (LLMs) and agentic approaches, IMAS aims to support Community Health Workers (CHWs).

![imas_flow](https://github.com/user-attachments/assets/f6c9deae-a2fd-4ea1-846d-e300e3ea36db)


## Abstract
Since the onset of COVID-19, rural communities worldwide have faced significant challenges in accessing healthcare due to the migration of experienced medical professionals to urban centers. Semi-trained caregivers, such as Community Health Workers (CHWs) and Registered Medical Practitioners (RMPs), have stepped in to fill this gap, but often lack formal training. This paper proposes an advanced agentic medical assistant system designed to improve healthcare delivery in rural areas by utilizing Large Language Models (LLMs) and agentic approaches. The system is composed of five crucial components: translation, medical complexity assessment, expert network integration, final medical advice generation, and response simplification. Our innovative framework ensures context-sensitive, adaptive, and reliable medical assistance, capable of clinical triaging, diagnostics, and identifying cases requiring specialist intervention. The system is designed to handle cultural nuances and varying literacy levels, providing clear and actionable medical advice in local languages. Evaluation results using the MedQA, PubMedQA, and JAMA datasets demonstrate that this integrated approach significantly enhances the effectiveness of rural healthcare workers, making healthcare more accessible and understandable for underserved populations.

## Models and Sources

| Model  | Souce of the Model| Purpose of the Model| Notes|
|----------|----------|----------|----------|
| Seamless M4T v2 Large  | [Hugging Face](https://huggingface.co/facebook/seamless-m4t-v2-large)   | For machine translation of prompts and responses   | The model was fine-tuned to include contextual and region-specific medical terminology.  |
|Medical Language Model  | [MLM](https://huggingface.co/meta-llama/Meta-Llama-3-70B)  | Instruction fine-tuned Llama-3-70B used as base model for clinical agents   | Fine-tuning datasets included multiturn dialog datasets, adverse events, clinical guidelines, and medical terminology  |

## Agents

| Agents   | Type of Agents | Skill Type | Base Model |
|----------|----------|----------|----------|
|  PCP  | Primary Care Provider   | A Primary Care Provider (PCP) possesses comprehensive clinical skills to diagnose, treat, and manage a wide range of health conditions, emphasizing preventive care and patient education   | MLM  |
| Complexity Assessment Agent  | Assess the complexity based on the clinical case details, Electronic Medical Records (EMR), etc. and classify the context   | Clinical case complexity assessment    | MLM  |
| Collaborative Diagnostic Agents    | Clinical Specilaist Agents representing different medical conditions| Clinical specialists like Encronologist, Cardiologist, Dietitian | MLM  |
| Response Simplification Agents    | Simplify medical responses to make them understandable for patients and healthcare workers by breaking down complex medical jargon into clear, concise, and actionable information, incorporating cultural sensitivity, providing step-by-step instructions, and implementing safeguards to prevent misinformation and ensure accuracy and safety.| Language simplification, Medical terminology transformation, Guardrails for disinformation / misinformation, and Cultural adaption | MLM  |

## Datasets
Below are the datasets used for evaluation.
- [MedQA](https://huggingface.co/datasets/bigbio/med_qa)
- [PubMedQA](https://huggingface.co/datasets/qiaojin/PubMedQA)
- [DDXPlus](https://huggingface.co/datasets/aai530-group6/ddxplus)
- [Clinical Guidelines](https://huggingface.co/datasets/epfl-llm/guidelines)
- [JAMA](https://github.com/xiaoman-zhang/PMC-VQA)

Please take a look at the [dataset directory](https://github.com/uheal/IMAS/tree/main/datasets) for more details.
## Results
![image](https://github.com/user-attachments/assets/916cad9b-dd0e-40e4-b28f-013ef1accd77)
