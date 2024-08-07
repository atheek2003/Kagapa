import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.SpeechText import logger
from src.SpeechText.pipeline.s_00_DENOISER_DNS_64 import AudioDenoising
# from src.SpeechText.pipeline.s_01_SPEECH_SEP import SpeechSeparation
from src.SpeechText.pipeline.s_01_AUDIO_SEGMENT import AudioSplitting
from src.SpeechText.pipeline.s_02_ASR_ADDY88 import AudioTranscription
from src.SpeechText.pipeline.s_03_PUNCT_PCS47LANG import TextPunctuation
from src.SpeechText.pipeline.s_04_TRANSLIT_OM import TextTransliteration
from src.SpeechText.pipeline.s_05_TRANSLATE_AI4BHARAT import TextTranslation
from src.SpeechText.pipeline.s_06_ENG_GRAMMAR_VENNIFY import GrammarCorrection

STAGE_NAME = "Stage 0 Audio Denoising"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    input_file = os.path.join(project_root, "artifacts", "INPUT", "input.mp3")
    output_dir = os.path.join(project_root, "artifacts", "STAGE_00")
    model_id = "addy88/wav2vec2-kannada-stt"
    target_lang = "kan"
    audio_denoising = AudioDenoising(input_file, output_dir, model_id, target_lang)
    audio_denoising.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e

# STAGE_NAME = "Stage 1 Speech Separation"
# try:
#     logger.info(f"********** {STAGE_NAME} started **********")
#     input_file = os.path.join(project_root, "artifacts", "STAGE_00", "Cleaned_denoiser_facebook_1_input.mp3")
#     output_dir = os.path.join(project_root, "artifacts", "STAGE_01")
#     speech_sep = SpeechSeparation(input_file, output_dir)
#     speech_sep.main()
#     logger.info(f"********** {STAGE_NAME} completed **********\n\n")
# except Exception as e:
#     logger.exception(e)
#     raise e

STAGE_NAME = "Stage 1 Audio Splitting"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    input_file = os.path.join(project_root, "artifacts", "STAGE_00", "Cleaned_denoiser_facebook_1_input.mp3")
    output_dir = os.path.join(project_root, "artifacts", "STAGE_01")
    audio_split = AudioSplitting(input_file, output_dir)
    audio_split.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Stage 2 Audio Transcription"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    audio_file = os.path.join(project_root, "artifacts", "STAGE_00", "Cleaned_denoiser_facebook_1_input.mp3")
    output_dir = os.path.join(project_root, "artifacts", "STAGE_02")
    model_id = "addy88/wav2vec2-kannada-stt"
    transcription = AudioTranscription(audio_file, output_dir, model_id)
    transcription.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Stage 3 Text Punctuation"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    input_file = os.path.join(project_root, "artifacts", "STAGE_02", "02_transcription.txt")
    output_dir = os.path.join(project_root, "artifacts", "STAGE_03")
    model_id = "pcs_47lang"
    punctuation = TextPunctuation(input_file, output_dir, model_id)
    punctuation.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Stage 4 Transliteration"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    input_file = os.path.join(project_root, "artifacts", "STAGE_03", "03_punctuation.txt")
    output_file = os.path.join(project_root, "artifacts", "STAGE_04", "04_transliteration.txt")
    transliteration = TextTransliteration(input_file, output_file)
    transliteration.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Stage 5 Translation"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    input_file = os.path.join(project_root, "artifacts", "STAGE_03", "03_punctuation.txt")
    output_file = os.path.join(project_root, "artifacts", "STAGE_05", "05_translation.txt")
    model_name = "ai4bharat/indictrans2-indic-en-1B"
    translation = TextTranslation(input_file, output_file, model_name)
    translation.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Stage 6 English Grammar Correction"
try:
    logger.info(f"********** {STAGE_NAME} started **********")
    input_file = os.path.join(project_root, "artifacts", "STAGE_05", "05_translation.txt")
    output_file = os.path.join(project_root, "artifacts", "STAGE_06", "06_english_grammar.txt")
    model_name = "vennify/t5-base-grammar-correction"
    grammar = GrammarCorrection(input_file, output_file, model_name)
    grammar.main()
    logger.info(f"********** {STAGE_NAME} completed **********\n\n")
except Exception as e:
    logger.exception(e)
    raise e

