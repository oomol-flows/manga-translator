# Manga Translator

**Transform your manga reading experience with AI-powered translation**

English | [中文](./README_zh.md)

---

## What is Manga Translator?

Manga Translator is an intelligent workflow tool that automatically translates manga pages and books from one language to another. Whether you're a manga enthusiast who wants to read content in your preferred language, or you need to translate manga for accessibility purposes, this tool makes the process simple and efficient.

## Key Features

✨ **Multi-Language Support**: Translate between 25+ languages including Japanese, English, Chinese (Simplified & Traditional), Spanish, French, German, Korean, and many more

🚀 **AI-Powered Translation**: Uses advanced AI models to provide accurate, context-aware translations that preserve the original meaning and style

📖 **Flexible Input Options**:
- Translate single manga pages
- Process entire manga books (multiple images)
- Handle various image formats (JPEG, PNG, GIF, BMP, TIFF, WebP)

⚡ **Hardware Acceleration**: Supports both CPU and CUDA (GPU) processing for faster translation speeds

🎯 **Smart Language Detection**: Automatically detects source language or allows manual specification

## How It Works

The Manga Translator uses sophisticated computer vision and natural language processing to:

1. **Detect Text**: Identifies text areas within manga images
2. **Extract Content**: Reads the original text using OCR (Optical Character Recognition)
3. **Translate**: Converts the text to your target language using AI translation models
4. **Replace**: Seamlessly replaces the original text with translated content while preserving the original layout and styling

## Available Workflows

### 📄 Single Page Translation
Perfect for translating individual manga pages or testing the translation quality.
- **Input**: Single manga page image
- **Output**: Translated image with same format
- **Use Case**: Quick translations, quality testing, single-page content

### 📚 Manga Book Translation
Ideal for translating complete manga chapters or entire books.
- **Input**: Multiple manga page images
- **Output**: Complete set of translated images
- **Use Case**: Full chapter translations, bulk processing, consistent styling across pages

### 🔄 Batch Processing
Advanced workflow for processing multiple manga books efficiently.
- **Input**: Multiple manga books (collections of images)
- **Output**: Organized translated manga collections
- **Use Case**: Large-scale translation projects, series processing

## Supported Languages

**Source Languages** (what you're translating from):
- Auto-detection available
- Japanese (日本語), Chinese (中文), Korean (한국어)
- English, Spanish, French, German, Italian
- And 15+ additional languages

**Target Languages** (what you're translating to):
- English, Spanish (Español), French (Français)
- German (Deutsch), Italian (Italiano)
- Chinese Simplified (简体中文), Chinese Traditional (繁體中文)
- Japanese (日本語), Korean (한국어)
- Portuguese, Russian, Arabic, Thai, Vietnamese
- And many more regional languages

## Who Can Use This?

- **Manga Readers**: Access manga in languages you understand
- **Content Creators**: Localize manga content for different audiences
- **Educators**: Use translated manga for language learning
- **Publishers**: Streamline the manga localization process
- **Accessibility Advocates**: Make manga content available to broader audiences

## Getting Started

1. **Choose Your Workflow**: Select single page, manga book, or batch processing based on your needs
2. **Upload Your Content**: Add your manga images to the workflow
3. **Select Languages**: Choose source language (or use auto-detection) and target language
4. **Configure Settings**: Adjust quality settings and hardware acceleration preferences
5. **Start Translation**: Run the workflow and receive your translated manga

## Technical Requirements

- **First Run**: The system will automatically download required AI models (this may take some time initially)
- **Hardware**: Works on both CPU and GPU (CUDA-enabled graphics cards for faster processing)
- **Internet**: Required for AI model downloads and translation services
- **Storage**: Ensure adequate space for original and translated images

## Quality and Accuracy

The translation quality depends on several factors:
- **Source Image Quality**: Higher resolution images produce better results
- **Text Clarity**: Clear, well-defined text translates more accurately
- **Language Pair**: Some language combinations work better than others
- **Context Complexity**: Simple dialogue translates more reliably than complex literary text

## Privacy and Security

- **Local Processing**: Core image processing happens on your device
- **AI Translation**: Uses secure, encrypted connections to translation services
- **No Data Storage**: Your manga content is not permanently stored on external servers
- **Token-Based**: Uses your OOMOL tokens for translation services

---

*Based on the powerful [manga-image-translator](https://github.com/zyddnys/manga-image-translator) project, enhanced for workflow-based processing.*

**Ready to start translating?** Simply load the workflow in your OOMOL platform and begin transforming your manga reading experience!