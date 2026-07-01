**final project Instruction**
For the final project you will work in groups of 4 on a research paper with sufficient quality to submitted to a top-tier NLP workshop. The goal is for you to become familiar with current NLP research and get hands-on experience working on emerging topics and tasks. There are 2 main avenues you can pursue: (i) developing a system for a **shared task evaluation** which involves building and evaluating models for understudied or novel tasks; or (ii) writing a **workshop paper** on a topic of interest to the NLP community, e.g., developing novel methods (or adapting existing ones) for some relevant task, critically evaluating state-of-the-art models, conducting insightful analyses, etc. Workshops serve primarily to report on preliminary results and work in progress and thus are not as selective as main conferences. See a list of workshops and shared tasks at the end of the instructions.

The project will have 3 main deliverables: a preliminary paper, a final paper, and a presentation (with a poster). Both papers should read like research papers with adequate formatting, organized into conventional sections, high quality illustrations (where needed), proper presentation of results (using figures and tables) and scholarly writing. The typical sections of a paper are: i) introduction/motivation/research questions; ii) background/related work; iii) methodology; iv) experiments; v) results; vi) conclusions/discussion; and vii) future work. Depending on the paper some sections might not make sense or some additional sections may need to be included. As in real-world conferences your work *must*  be submitted using the appropriate templates (provided below), otherwise it will not be accepted. **Note that the papers are the most visible parts of your work and as such they should reflect what you have done**.  

Good writing takes time and it is hard to get started so don’t leave it to the last minute! If you have never wrote a scientific paper before, don’t worry. Like any other skill, practice makes progress! Reading a lot of high-quality papers is also very helpful. In any case, I *strongly* recommend this tutorial on writing NLP/AI/ML papers by Noah Smith and these tips on writing NLP papers.
**Mentorship and effort/mastery**

This project will be conducted under the mentorship of the instructors, meaning that we will have regular project meetings to assess progress and discuss next steps. We will meet weekly or every other week depending on the number of groups. Regular meetings will encourage consistent progress and give you an opportunity to get timely feedback, avoid roadblocks and maximize your chances of turning in high quality work. At the same time, these meetings will allow us to assess your effort and mastery on your chosen topic of research. Note that this will be an important component of your final grade. To be clear, there is an inherent degree of subjectivity when assigning a discrete grade to effort/mastery. However, by meeting regularly you will get continuous feedback and opportunities to course correct if needed.

**Google Cloud Compute Credits**

To help you execute your projects, we provide google cloud credits which you can redeem via this `link (coming soon)`. This will give you access to GPUs/TPUs on Google Colab.  Note that the vouchers have a value of $50 so you will need to manage this compute budget accordingly. Consider running small scale experiments during development (that can run without GPUs) and then scale things up when you are certain that they are working as intended. 

**Generative AI**

You are allowed to use coding assistants to help on the development of your experimental workbench, model implementation, etc., but you are responsible for the code and must be knowledgeable of the codebase. In regards to the papers, ALL WRITING MUST BE YOUR OWN. There is certainly utility in using LLMs to sketch and improve drafts but writing down your ideas and summarizing papers in your own words is a powerful way of organizing and clarifying your thoughts and ideas, and to find gaps in your knowledge. This effort will in turn help you gain mastery of the subject.

## Task 0: Project Proposal (ungraded)

1. Pick a shared task or workshop to work on from the list provided below. If there is something else you would like to work on that does not fit on any of the workshops please talk to us beforehand. Then find and read at least 8 related papers (2 papers per group member) to include in your related work section (these can be a mix of papers describing the models you are going to use and prior work on your chosen task/problem). There are a lot of papers out there! Pleasure make sure that whatever you are reading comes from a reputable conference/journal. Here is a list of the top venues in NLP. These are not the only sources of good papers so if you are unsure reach out to us.
2. Write down your plan as described below
### Plan

Your proposal should be approximately 1 page (single-spaced), and briefly describe your project. Be sure to answer all relevant questions, including but not limited to:

1. What is the task/goal/research questions of the paper?
2. Most importantly: what is your data? (identify  dataset(s) for this step and describe them in detail). IMPORTANT NOTE: use only use existing datasets! Creating a dataset yourself will take way more time than you may think and it is beyond the scope of this class. 
3. What tools will you be using?
4. What models will you be using?
    1. Which of these will you be implementing yourself vs. using models provided in packages?
    2. Identify  specific options if you are using models from implemented packages (e.g., the main hyperparameters for the models you will use)
    3. How will you evaluate your model/solution?
5. Which papers are you going to include in your related work section. For each paper, explain in 1-2 sentences why do you want to include it in your review.
6. Any other resources that you’ll need to use? Components you’ll need to implement?
7. What visualizations/results/etc will you be producing?
8. What is your timeline/working plan?
9. Who in your group will be in charge of which component?

Note that your proposal should be a narrative that covers these points NOT bullet points with direct answers to these questions. Feel free to add other points that help make clear your goals and plan of action. 

## Task 1: Preliminary Report

The preliminary report should be an extension of your project proposal with an emphasis on expanding the literature review to include at least 20-24 papers (5-6 papers per group member). The included papers should be summarized and discussed ***in the context*** of your work (i.e., you must articulate how it relates to your work, in what ways is it similar/different, how it provides a foundation/baseline for what you are doing, etc.). You should also include some exploratory data analysis and preliminary results with simple baselines. This will ensure that you are on track to complete the project and help identify potential issues and roadblocks early on. The report should use the provided `[template]`  and cannot exceed 4 pages (excluding references and appendices). Submissions made without the correct template will get 0.

## Task 2: Final Paper

Submit a 8-page paper (excluding citations and appendices) using this `[template]`. Feel free to add additional results and details to the appendix but make sure that your work can stand on its own given the content in the main paper (i.e., don’t put key results and details on the appendix). Submissions made without the correct template will get 0. Your final report should read like a research paper and include the usual sections (described above).  ****Note that you may need to summarize some of your literature review to fit into the related work section. Your final paper should clearly describe:

1. Abstract (brief summary of the paper in a few sentences)
2. Introduction (Introduce the problem at a high-level in the context of existing work, overview of your proposed approach, articulate the structure of the paper and key contributions)
3. The problem (What is the problem you are trying to solve and why is it interesting?)
4. Main idea (What is the key idea/contribution?)
5. Details/Evaluation/Results 
6. Related work 
7. Conclusions and further work
## Task 3: Presentation

Prepare a poster and record a video presentation of your work that does not exceed 8 minutes (hard cutoff — work will be judged on the first 8 minutes of the presentation and points will be deducted for exceeding the time). Make sure that all group members have the opportunity to talk. Ideally, each group member should talk about the parts of the work they were most responsible for. **You must submit your poster to Gradescope and upload your video to google drive (youtube, or other easily accessible video hosting platform will also work). You can add a link/qr code to the recording in the poster.**

You will also present your work to your colleagues in class. This will be an opportunity to showcase your work and answer questions. After the presentations, all students will vote on their favorite projects. The top 3 projects will get receive an additional 15% points of extra-credit.

## Final Grade

The final project’s grade breakdown is as follows:

- Preliminary Paper: 20%
- Final Paper: 40%
- Presentation: 15%
- Effort/Mastery: 25%
- Outstanding project: +15% extra-credit (spills over to final grade)



Here is a list of recent shared tasks and workshops held in top-tier conferences. For the workshops, we also linked the proceedings of the last edition for you to see what kinds of papers get accepted. Hopefully this will give you some inspiration on topics to pursue or follow-up work (e.g., the future work suggested in the papers.


| Workshop | Proceedings |
| --- | --- |
| [Workshop on Language and Language Models (WoLaLa)](https://wolala.nytud.hu/2026/programme/) |  |
| [GeBNLP (Workshop on Gender Bias in Natural Language Processing)](https://gebnlp-workshop.github.io/2025/cfp.html) |  |
| [Workshop on Scholarly Document Processing](https://sdproc.org/2025/) | [proceedings](https://aclanthology.org/volumes/2025.sdp-1/) |
| [Multilingual and Multicultural Evaluation (MME)](https://multilingual-multicultural-evaluation.github.io/) | [proceedings](https://aclanthology.org/volumes/2026.mme-main/) |
| [Natural Language Processing for Political Sciences](https://aclanthology.org/events/politicalnlp-2024/) |  |
| [Political NLP](http://lrec-conf.org/proceedings/lrec2026/workshops/politicalnlp/2026.politicalnlp-1.0.pdf) |  |
| [CL4Health](http://lrec-conf.org/proceedings/lrec2026/workshops/cl4health/2026.cl4health-1.0.pdf) |  |
| [Identity-Aware AI](http://lrec-conf.org/proceedings/lrec2026/workshops/iaai/2026.iaai-1.0.pdf) |  |
| [NLP4ECOLOGY](https://aclanthology.org/volumes/2025.nlp4ecology-1/) |  |
| [Workshop on Text Simplification, Accessibility and Readability](https://tsar-workshop.github.io/) | [proceedings](https://aclanthology.org/2025.tsar-1.0/) |
| [Language Technology for Equality, Diversity and Inclusion:](https://sites.google.com/view/lt-edi-2026/home) | [proceedings](https://aclanthology.org/volumes/2025.ltedi-1/) |
| [Natural Language Processing for Digital Humanities (NLP4DH)](https://www.nlp4dh.com/nlp4dh-2026) | [proceedings](https://aclanthology.org/volumes/2025.nlp4dh-1/) |
| [CLPsych](https://clpsych.org/shared-task/) | [proceedings](https://aclanthology.org/volumes/2024.customnlp4u-1/) |
| [Towards Knowledgeable Foundation Models](https://knowledgeable-lm.github.io/) | [proceedings](https://aclanthology.org/2025.knowllm-1.0/) |
| [AmericasNLP](https://turing.iimas.unam.mx/americasnlp/2026_workshop.html) | [proceedings](https://aclanthology.org/volumes/2025.americasnlp-1/) |
| [Language Models for Low-Resource Languages](https://loreslm.github.io/) | [proceedings](https://aclanthology.org/volumes/2025.loreslm-1/) |
| Workshop on Online Abuse and Harms | [proceedings](https://aclanthology.org/volumes/2025.woah-1/) |
| [NLP for Positive Impact](https://sites.google.com/view/nlp4positiveimpact) | [proceedings](https://aclanthology.org/events/nlp4pi-2025/) |
| Student Research Workshop @ ACL | [proceedings](https://aclanthology.org/volumes/2025.acl-srw/) |
| Workshop on Games and Natural Language Processing | [proceedings](http://www.lrec-conf.org/proceedings/lrec2022/workshops/Games/index.html) |
| [Workshop on Computational Approaches to Subjectivity, Sentiment & Social Media Analysis](https://workshop-wassa.github.io/) | [proceedings](https://aclanthology.org/events/wassa-2024/) |
| [Technologies for Machine Translation of Low-Resource Languages (LoResMT)](https://www.loresmt.org/) | [proceedings](https://aclanthology.org/volumes/2026.loresmt-1/) |




See a list of fairly recent shared tasks. Note that in some cases there are multiple tasks: either prior editions, multiple related tasks or sub-tasks. Make sure that you are able to access everything you need to “participate”, including: train/test data, evaluation metrics and/or related scripts (official submission is not required).
| **Shared Task** |
| --- |
| [Scholarly Document Processing](https://sdproc.org/2025/sharedtasks.html) |
| [Text Simplification, Accessibility and Readability](https://tsar-workshop.github.io/shared-task/) |
| [CL4Health](https://bionlp.nlm.nih.gov/cl4health2026/#st) |
| [SemEval](https://semeval.github.io/) |
| [CONNL Shared tasks](https://www.conll.org/previous-tasks) |
| [Language Technology for Equality, Diversity and Inclusion](https://sites.google.com/view/lt-edi-2026/shared-tasks) |
| [AmericasNLP](https://turing.iimas.unam.mx/americasnlp/2026_st.html) |
| [Workshop on Computational Approaches to Subjectivity, Sentiment & Social Media Analysis](https://workshop-wassa.github.io/2024/shared_task/) |
| [BabyLM Challenge](https://babylm.github.io/) |

Other resources to find papers:

-   [Google Scholar](https://scholar.google.com/)
-   [ACL Anthology](https://aclanthology.org/)
-   [Semantic Scholar](https://www.semanticscholar.org/)
-   [Asta Paper Finder](https://asta.allen.ai/discover)