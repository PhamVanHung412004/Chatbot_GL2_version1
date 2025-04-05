import numpy as np
import pandas as pd
import faiss
import torch
import json
from groq import Groq
import os
import ast
import webbrowser

from langdetect import detect,LangDetectException
from deep_translator import GoogleTranslator

from transformers import AutoModelForCausalLM, AutoTokenizer
from read_file import *
from convert_embedding import Embedding_To_Numpy
from pathlib import Path
from sentence_transformers import SentenceTransformer
from Input import Init_Input
from semantic_search import Sematic_search
from gen import Answer_Question_From_Documents