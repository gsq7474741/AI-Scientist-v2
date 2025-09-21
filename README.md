<div align="center">
  <a href="https://github.com/SakanaAI/AI-Scientist_v2/blob/main/docs/logo_v1.jpg">
    <img src="docs/logo_v1.png" width="215" alt="AI Scientist v2 Logo" />
  </a>
  <h1>
    <b>The AI Scientist-v2: Workshop-Level Automated</b><br>
    <b>Scientific Discovery via Agentic Tree Search</b>
  </h1>
</div>

<p align="center">
  📚 <a href="https://pub.sakana.ai/ai-scientist-v2/paper">[Paper]</a> |
  📝 <a href="https://sakana.ai/ai-scientist-first-publication/"> [Blog Post]</a> |
  📂 <a href="https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment"> [ICLR2025 Workshop Experiment]</a>
</p>

Fully autonomous scientific research systems are becoming increasingly capable, with AI playing a pivotal role in transforming how scientific discoveries are made.
We are excited to introduce The AI Scientist-v2, a generalized end-to-end agentic system that has generated the first workshop paper written entirely by AI and accepted through peer review.

This system autonomously generates hypotheses, runs experiments, analyzes data, and writes scientific manuscripts. Unlike [its predecessor (AI Scientist-v1)](https://github.com/SakanaAI/AI-Scientist), the AI Scientist-v2 removes reliance on human-authored templates, generalizes across Machine Learning (ML) domains, and employs a progressive agentic tree search, guided by an experiment manager agent.

> **Note:**
> The AI Scientist-v2 doesn’t necessarily produce better papers than v1, especially when a strong starting template is available. v1 follows well-defined templates, leading to high success rates, while v2 takes a broader, more exploratory approach with lower success rates. v1 works best for tasks with clear objectives and a solid foundation, whereas v2 is designed for open-ended scientific exploration.

> **Caution!**
> This codebase will execute Large Language Model (LLM)-written code. There are various risks and challenges associated with this autonomy, including the potential use of dangerous packages, uncontrolled web access, and the possibility of spawning unintended processes. Ensure that you run this within a controlled sandbox environment (e.g., a Docker container). Use at your own discretion.

## Table of Contents

1.  [Requirements](#requirements)
    *   [Installation](#installation)
    *   [Supported Models and API Keys](#supported-models-and-api-keys)
2.  [Generate Research Ideas](#generate-research-ideas)
3.  [Run AI Scientist-v2 Paper Generation Experiments](#run-ai-scientist-v2-paper-generation-experiments)
4.  [Citing The AI Scientist-v2](#citing-the-ai-scientist-v2)
5.  [Frequently Asked Questions](#frequently-asked-questions)
6.  [Acknowledgement](#acknowledgement)

## Requirements

This code is designed to run on Linux with NVIDIA GPUs using CUDA and PyTorch.

### Installation

```bash
# Create a new conda environment
conda create -n ai_scientist python=3.11
conda activate ai_scientist

# Install PyTorch with CUDA support (adjust pytorch-cuda version for your setup)
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia

# Install PDF and LaTeX tools
conda install anaconda::poppler
conda install conda-forge::chktex

# Install Python package requirements
pip install -r requirements.txt
```

Installation usually takes no more than one hour.

### Supported Models and API Keys

#### OpenAI Models

By default, the system uses the `OPENAI_API_KEY` environment variable for OpenAI models.

#### Gemini Models

By default, the system uses the `GEMINI_API_KEY` environment variable for Gemini models through OpenAI API.

#### Claude (Native Anthropic API) with optional Custom Base

This project uses the native Anthropic Claude Messages API. You can also route requests through a custom reverse proxy or gateway by providing a custom base URL.

Environment variables:

```bash
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_KEY"
# Optional: use a custom base URL (reverse proxy or gateway compatible with Anthropic SDK)
export CLAUDE_API_BASE="https://your-proxy.example.com"
```

Supported native Claude model IDs include (non-exhaustive):

```
claude-3-5-sonnet-20240620
claude-3-5-sonnet-20241022
claude-3-sonnet-20240229
claude-3-haiku-20240307
claude-3-opus-20240229
claude-opus-4-0
claude-sonnet-4-0
claude-3-7-sonnet-latest
```

#### Semantic Scholar API (Literature Search)

Our code can optionally use a Semantic Scholar API Key (`S2_API_KEY`) for higher throughput during literature search [if you have one](https://www.semanticscholar.org/product/api). This is used during both the ideation and paper writing stages. The system should work without it, though you might encounter rate limits or reduced novelty checking during ideation. If you experience issues with Semantic Scholar, you can skip the citation phase during paper generation.

#### Setting API Keys

Ensure you provide the necessary API keys as environment variables for the models you intend to use. For example:
```bash
export OPENAI_API_KEY="YOUR_OPENAI_KEY_HERE"
export S2_API_KEY="YOUR_S2_KEY_HERE"
# For Anthropic Claude (native)
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_KEY"
# Optional custom base URL for Claude
# export CLAUDE_API_BASE="https://your-proxy.example.com"
```

## Generate Research Ideas

Before running the full AI Scientist-v2 experiment pipeline, you first use the `ai_scientist/perform_ideation_temp_free.py` script to generate potential research ideas. This script uses an LLM to brainstorm and refine ideas based on a high-level topic description you provide, interacting with tools like Semantic Scholar to check for novelty.

1.  **Prepare a Topic Description:** Create a Markdown file (e.g., `my_research_topic.md`) describing the research area or theme you want the AI to explore. This file should contain sections like `Title`, `Keywords`, `TL;DR`, and `Abstract` to define the scope of the research. Refer to the example file `ai_scientist/ideas/i_cant_believe_its_not_better.md` for the expected structure and content format. Place your file in a location accessible by the script (e.g., the `ai_scientist/ideas/` directory).

2.  **Run the Ideation Script:** Execute the script from the main project directory, pointing it to your topic description file and specifying the desired LLM.

    ```bash
    python ai_scientist/perform_ideation_temp_free.py \
     --workshop-file "ai_scientist/ideas/my_research_topic.md" \
     --model gpt-4o-2024-05-13 \
     --max-num-generations 20 \
     --num-reflections 5
    ```
    *   `--workshop-file`: Path to your topic description Markdown file.
    *   `--model`: The LLM to use for generating ideas (ensure you have the corresponding API key set).
    *   `--max-num-generations`: How many distinct research ideas to attempt generating.
    *   `--num-reflections`: How many refinement steps the LLM should perform for each idea.

3.  **Output:** The script will generate a JSON file named after your input Markdown file (e.g., `ai_scientist/ideas/my_research_topic.json`). This file will contain a list of structured research ideas, including hypotheses, proposed experiments, and related work analysis.

4.  **Proceed to Experiments:** Once you have the generated JSON file containing research ideas, you can proceed to the next section to run the experiments.

This ideation step guides the AI Scientist towards specific areas of interest and produces concrete research directions to be tested in the main experimental pipeline.

## Run AI Scientist-v2 Paper Generation Experiments

Using the JSON file generated in the previous ideation step, you can now launch the main AI Scientist-v2 pipeline. This involves running experiments via agentic tree search, analyzing results, and generating a paper draft.

Specify the models used for the write-up and review phases via command-line arguments.
The configuration for the best-first tree search (BFTS) is located in `bfts_config.yaml`. Adjust parameters in this file as needed.

Key tree search configuration parameters in `bfts_config.yaml`:

-   `agent` config:
    -   Set `num_workers` (number of parallel exploration paths) and `steps` (maximum number of nodes to explore). For example, if `num_workers=3` and `steps=21`, the tree search will explore up to 21 nodes, expanding 3 nodes concurrently at each step.
    -   `num_seeds`: Should generally be the same as `num_workers` if `num_workers` is less than 3. Otherwise, set `num_seeds` to 3.
    -   Note: Other agent parameters like `k_fold_validation`, `expose_prediction`, and `data_preview` are not used in the current version.
-   `search` config:
    -   `max_debug_depth`: The maximum number of times the agent will attempt to debug a failing node before abandoning that search path.
    -   `debug_prob`: The probability of attempting to debug a failing node.
    -   `num_drafts`: The number of initial root nodes (i.e., the number of independent trees to grow) during Stage 1.

Example command to run AI-Scientist-v2 using a generated idea file (e.g., `my_research_topic.json`). Please review `bfts_config.yaml` for detailed tree search parameters (the default config includes `claude-3-5-sonnet` for experiments). Do not set `load_code` if you do not want to initialize experimentation with a code snippet.

```bash
python launch_scientist_bfts.py \
 --load_ideas "ai_scientist/ideas/my_research_topic.json" \
 --load_code \
 --add_dataset_ref \
 --model_writeup o1-preview-2024-09-12 \
 --model_citation gpt-4o-2024-11-20 \
 --model_review gpt-4o-2024-11-20 \
 --model_agg_plots o3-mini-2025-01-31 \
 --num_cite_rounds 20
```

Once the initial experimental stage is complete, you will find a timestamped log folder inside the `experiments/` directory. Navigate to `experiments/"timestamp_ideaname"/logs/0-run/` within that folder to find the tree visualization file `unified_tree_viz.html`.
After all experiment stages are complete, the writeup stage begins. The writeup stage typically takes about 20 to 30 minutes in total. Once it finishes, you should see `timestamp_ideaname.pdf` in the `timestamp_ideaname` folder.
For this example run, all stages typically finish within several hours.

## Citing The AI Scientist-v2

If you use **The AI Scientist-v2** in your research, please cite our work as follows:

```bibtex
@article{aiscientist_v2,
  title={The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search},
  author={Yamada, Yutaro and Lange, Robert Tjarko and Lu, Cong and Hu, Shengran and Lu, Chris and Foerster, Jakob and Clune, Jeff and Ha, David},
  journal={arXiv preprint arXiv:2504.08066},
  year={2025}
}
```

## Frequently Asked Questions

**Why wasn't a PDF or a review generated for my experiment?**

The AI Scientist-v2 completes experiments with a success rate that depends on the chosen foundation model, and the complexity of the idea. Higher success rates are generally observed when using powerful models like Claude 3.5 Sonnet for the experimentation phase.

**What is the estimated cost per experiment?**

The ideation step cost depends on the LLM used and the number of generations/reflections, but is generally low (a few dollars). For the main experiment pipeline, using Claude 3.5 Sonnet for the experimentation phase typically costs around $15–$20 per run. The subsequent writing phase adds approximately $5 when using the default models specified in the example command. Using GPT-4o for `model_citation` is recommended as it can help reduce writing costs.

**How do I run The AI Scientist-v2 for different subject fields?**

First, perform the [Generate Research Ideas](#generate-research-ideas) step. Create a new Markdown file describing your desired subject field or topic, following the structure of the example `ai_scientist/ideas/i_cant_believe_its_not_better.md`. Run the `perform_ideation_temp_free.py` script with this file to generate a corresponding JSON idea file. Then, proceed to the [Run AI Scientist-v2 Paper Generation Experiments](#run-ai-scientist-v2-paper-generation-experiments) step, using this JSON file with the `launch_scientist_bfts.py` script via the `--load_ideas` argument.

**What should I do if I have problems accessing the Semantic Scholar API?**

The Semantic Scholar API is used to assess the novelty of generated ideas and to gather citations during the paper write-up phase. If you don't have an API key, encounter rate limits, you may be able to skip these phases.

**I encountered a "CUDA Out of Memory" error. What can I do?**

This error typically occurs when the AI Scientist-v2 attempts to load or run a model that requires more GPU memory than available on your system. To resolve this, you can try updating your ideation prompt file (`ai_scientist/ideas/my_research_topic.md`) to suggest using smaller models for the experiments.

## Acknowledgement

The tree search component implemented within the `ai_scientist` directory is built on top of the [AIDE](https://github.com/WecoAI/aideml) project. We thank the AIDE developers for their valuable contributions and for making their work publicly available.


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SakanaAI/AI-Scientist-v2&type=Date)](https://star-history.com/#SakanaAI/AI-Scientist-v2&Date)

帮我把以下信息做成一个配置文件，使该项目能够加载，类似于node技术栈中dot-env和.env文件的形式
openai 协议: https//api.openai-proxy.org/v1
  - 支持openai所有模型
  - 支持deepseek模型
anthropic apibase： https://api.openai-proxy.org/anthropic
  - 支持anthropic所有模型
gemini协议：https://api.openai-proxy.org/google
  - 支持gemini所有模型
秘钥 sk-9tbQSdt1iL0rJW31DFS3rMKxH8NUIBUwE4cC2OkF7tCVNoqB

并把以下模型列表整理成一个markdown，然后看看这些模型的选择怎么集成到项目中（我记得gpt5和以前gpt模型的接口不一样了，需要重新适配）
具体模型列表
模型	类型	模型限流	
定价(美元)
gpt-5-2025-08-07 最新上线	chat	500 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-5-chat-latest 最新上线	chat	500 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-5-mini 最新上线	chat	1000 RPM	
输入价格: 
$0.25
×1.5
/ M Tokens
输出价格: 
$2
×1.5
/ M Tokens
gpt-5-mini-2025-08-07 最新上线	chat	1000 RPM	
输入价格: 
$0.25
×1.5
/ M Tokens
输出价格: 
$2
×1.5
/ M Tokens
gpt-5-nano 最新上线	chat	1000 RPM	
输入价格: 
$0.05
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gpt-5-nano-2025-08-07 最新上线	chat	1000 RPM	
输入价格: 
$0.05
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gpt-5 最新上线	chat	500 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
o4-mini-deep-research-2025-06-26 最新上线	chat	1000 RPM	
输入价格: 
$2
×1.5
/ M Tokens
输出价格: 
$8
×1.5
/ M Tokens
o4-mini-deep-research 最新上线	chat	1000 RPM	
输入价格: 
$2
×1.5
/ M Tokens
输出价格: 
$8
×1.5
/ M Tokens
o3-deep-research-2025-06-26 最新上线	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$40
×1.5
/ M Tokens
o3-deep-research 最新上线	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$40
×1.5
/ M Tokens
o3-pro-2025-06-10	chat	500 RPM	
输入价格: 
$20
×1.5
/ M Tokens
输出价格: 
$80
×1.5
/ M Tokens
o3-pro	chat	500 RPM	
输入价格: 
$20
×1.5
/ M Tokens
输出价格: 
$80
×1.5
/ M Tokens
gpt-4o-audio-preview-2025-06-03	chat	100 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
o4-mini-2025-04-16	chat	1000 RPM	
输入价格: 
$1.1
×1.5
/ M Tokens
输出价格: 
$4.4
×1.5
/ M Tokens
o4-mini	chat	1000 RPM	
输入价格: 
$1.1
×1.5
/ M Tokens
输出价格: 
$4.4
×1.5
/ M Tokens
o3-2025-04-16	chat	500 RPM	
输入价格: 
$2
×1.5
/ M Tokens
输出价格: 
$8
×1.5
/ M Tokens
o3	chat	500 RPM	
输入价格: 
$2
×1.5
/ M Tokens
输出价格: 
$8
×1.5
/ M Tokens
gpt-4.1-nano-2025-04-14	chat	1000 RPM	
输入价格: 
$0.1
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gpt-4.1-nano	chat	1000 RPM	
输入价格: 
$0.1
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gpt-4.1-mini-2025-04-14	chat	1000 RPM	
输入价格: 
$0.4
×1.5
/ M Tokens
输出价格: 
$1.6
×1.5
/ M Tokens
gpt-4.1-mini	chat	1000 RPM	
输入价格: 
$0.4
×1.5
/ M Tokens
输出价格: 
$1.6
×1.5
/ M Tokens
gpt-4.1-2025-04-14	chat	1000 RPM	
输入价格: 
$2
×1.5
/ M Tokens
输出价格: 
$8
×1.5
/ M Tokens
gpt-4.1	chat	1000 RPM	
输入价格: 
$2
×1.5
/ M Tokens
输出价格: 
$8
×1.5
/ M Tokens
gpt-4o-mini-search-preview	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$0.6
×1.5
/ M Tokens
gpt-4o-mini-search-preview-2025-03-11	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$0.6
×1.5
/ M Tokens
gpt-4o-search-preview	chat	200 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-4o-search-preview-2025-03-11	chat	200 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
computer-use-preview	chat	200 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$12
×1.5
/ M Tokens
computer-use-preview-2025-03-11	chat	200 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$12
×1.5
/ M Tokens
o1-pro	chat	200 RPM	
输入价格: 
$150
×1.5
/ M Tokens
输出价格: 
$600
×1.5
/ M Tokens
o1-pro-2025-03-19	chat	200 RPM	
输入价格: 
$150
×1.5
/ M Tokens
输出价格: 
$600
×1.5
/ M Tokens
gpt-4.5-preview	chat	100 RPM	
输入价格: 
$75
×1.5
/ M Tokens
输出价格: 
$150
×1.5
/ M Tokens
gpt-4.5-preview-2025-02-27	chat	100 RPM	
输入价格: 
$75
×1.5
/ M Tokens
输出价格: 
$150
×1.5
/ M Tokens
o3-mini	chat	1000 RPM	
输入价格: 
$1.1
×1.5
/ M Tokens
输出价格: 
$4.4
×1.5
/ M Tokens
o3-mini-2025-01-31	chat	1000 RPM	
输入价格: 
$1.1
×1.5
/ M Tokens
输出价格: 
$4.4
×1.5
/ M Tokens
gpt-4o-mini-audio-preview-2024-12-17	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$0.6
×1.5
/ M Tokens
gpt-4o-mini-audio-preview	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$0.6
×1.5
/ M Tokens
gpt-4o-audio-preview-2024-12-17	chat	100 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
o1	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
o1-2024-12-17	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
gpt-4o-2024-11-20	chat	500 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-4o-audio-preview	chat	100 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-4o-audio-preview-2024-10-01	chat	100 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
o1-mini	chat	1000 RPM	
输入价格: 
$1.1
×1.5
/ M Tokens
输出价格: 
$4.4
×1.5
/ M Tokens
o1-mini-2024-09-12	chat	1000 RPM	
输入价格: 
$1.1
×1.5
/ M Tokens
输出价格: 
$4.4
×1.5
/ M Tokens
o1-preview	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
o1-preview-2024-09-12	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
chatgpt-4o-latest	chat	500 RPM	
输入价格: 
$5
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
gpt-4o-2024-08-06	chat	500 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-4o-mini	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$0.6
×1.5
/ M Tokens
gpt-4o-mini-2024-07-18	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$0.6
×1.5
/ M Tokens
gpt-4o-2024-05-13	chat	500 RPM	
输入价格: 
$5
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
gpt-4o	chat	500 RPM	
输入价格: 
$2.5
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gpt-4-turbo	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-turbo-2024-04-09	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-0125-preview	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-1106-preview	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-1106-vision-preview	chat	200 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-turbo-preview	chat	500 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-vision-preview	chat	200 RPM	
输入价格: 
$10
×1.5
/ M Tokens
输出价格: 
$30
×1.5
/ M Tokens
gpt-4-32k	chat	200 RPM	
输入价格: 
$60
×1.5
/ M Tokens
输出价格: 
$120
×1.5
/ M Tokens
gpt-4-32k-0314	chat	200 RPM	
输入价格: 
$60
×1.5
/ M Tokens
输出价格: 
$120
×1.5
/ M Tokens
gpt-4-32k-0613	chat	200 RPM	
输入价格: 
$60
×1.5
/ M Tokens
输出价格: 
$120
×1.5
/ M Tokens
gpt-4	chat	500 RPM	
输入价格: 
$30
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
gpt-4-0314	chat	500 RPM	
输入价格: 
$30
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
gpt-4-0613	chat	500 RPM	
输入价格: 
$30
×1.5
/ M Tokens
输出价格: 
$60
×1.5
/ M Tokens
gpt-3.5-turbo	chat	1000 RPM	
输入价格: 
$0.5
×1.5
/ M Tokens
输出价格: 
$1.5
×1.5
/ M Tokens
gpt-3.5-turbo-0125	chat	1000 RPM	
输入价格: 
$0.5
×1.5
/ M Tokens
输出价格: 
$1.5
×1.5
/ M Tokens
gpt-3.5-turbo-0301 已废弃	chat	1000 RPM	
输入价格: 
$1.5
×1.5
/ M Tokens
输出价格: 
$2
×1.5
/ M Tokens
gpt-3.5-turbo-0613 已废弃	chat	1000 RPM	
输入价格: 
$1.5
×1.5
/ M Tokens
输出价格: 
$2
×1.5
/ M Tokens
gpt-3.5-turbo-1106	chat	1000 RPM	
输入价格: 
$1
×1.5
/ M Tokens
输出价格: 
$2
×1.5
/ M Tokens
gpt-3.5-turbo-16k 已废弃	chat	1000 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$4
×1.5
/ M Tokens
gpt-3.5-turbo-16k-0613 已废弃	chat	1000 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$4
×1.5
/ M Tokens


模型	类型	模型限流	
定价(美元)
claude-opus-4-1-20250805 最新上线	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$75
×1.5
/ M Tokens
claude-opus-4-0	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$75
×1.5
/ M Tokens
claude-opus-4-20250514	chat	500 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$75
×1.5
/ M Tokens
claude-sonnet-4-0	chat	500 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-sonnet-4-20250514	chat	500 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-3-7-sonnet-20250219	chat	500 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-3-7-sonnet-latest	chat	500 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-3-5-haiku-20241022	chat	1000 RPM	
输入价格: 
$1
×1.5
/ M Tokens
输出价格: 
$5
×1.5
/ M Tokens
claude-3-5-haiku-latest	chat	1000 RPM	
输入价格: 
$1
×1.5
/ M Tokens
输出价格: 
$5
×1.5
/ M Tokens
claude-3-5-sonnet-20241022	chat	1000 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-3-5-sonnet-latest	chat	1000 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-3-5-sonnet-20240620	chat	1000 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens
claude-3-haiku-20240307	chat	1000 RPM	
输入价格: 
$0.25
×1.5
/ M Tokens
输出价格: 
$1.25
×1.5
/ M Tokens
claude-3-opus-20240229	chat	1000 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$75
×1.5
/ M Tokens
claude-3-opus-latest	chat	1000 RPM	
输入价格: 
$15
×1.5
/ M Tokens
输出价格: 
$75
×1.5
/ M Tokens
claude-3-sonnet-20240229	chat	1000 RPM	
输入价格: 
$3
×1.5
/ M Tokens
输出价格: 
$15
×1.5
/ M Tokens



模型	类型	模型限流	
定价(美元)
gemini-2.5-flash-image-preview 最新上线	chat	1000 RPM	
输入价格: 
$0.3
×1.5
/ M Tokens
输出价格: 
$2.5
×1.5
/ M Tokens
gemini-2.5-flash	chat	1000 RPM	
输入价格: 
$0.3
×1.5
/ M Tokens
输出价格: 
$2.5
×1.5
/ M Tokens
gemini-2.5-flash-lite	chat	1000 RPM	
输入价格: 
$0.1
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gemini-2.5-flash-lite-preview-06-17	chat	1000 RPM	
输入价格: 
$0.1
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gemini-2.5-pro	chat	1000 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gemini-2.5-pro-preview-06-05 已废弃	chat	1000 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gemini-2.0-flash-preview-image-generation	chat	1000 RPM	
输入价格: 
$0.1
×1.5
/ M Tokens
输出价格: 
$0.4
×1.5
/ M Tokens
gemini-2.5-flash-preview-05-20	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$3.5
×1.5
/ M Tokens
gemini-2.5-pro-preview-05-06	chat	1000 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gemini-2.5-flash-preview-04-17	chat	1000 RPM	
输入价格: 
$0.15
×1.5
/ M Tokens
输出价格: 
$3.5
×1.5
/ M Tokens
gemini-2.5-pro-preview-03-25	chat	1000 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens
gemini-2.5-pro-exp-03-25 已废弃	chat	1000 RPM	
输入价格: 
$1.25
×1.5
/ M Tokens
输出价格: 
$10
×1.5
/ M Tokens


模型	类型	模型限流	
定价(美元)
deepseek-chat	chat	1000 RPM	
输入价格: 
$0.55
×1.5
/ M Tokens
输出价格: 
$1.7
×1.5
/ M Tokens
deepseek-reasoner	chat	1000 RPM	
输入价格: 
$0.55
×1.5
/ M Tokens
输出价格: 
$1.7
×1.5
/ M Tokens
