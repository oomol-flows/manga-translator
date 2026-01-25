# Manga Translator

**Break down language barriers and enjoy manga in any language you prefer**

English | [中文](./README_zh-CN.md)

---

## What is Manga Translator?

Manga Translator is a powerful tool that automatically converts manga from one language to another. It understands the text in your manga images, translates it into your chosen language, and seamlessly replaces the original text while preserving the artwork and layout. Whether you want to read Japanese manga in English, translate Chinese comics to Spanish, or make any manga accessible in your native language, this tool handles it all effortlessly.

## Why Use Manga Translator?

✨ **Read Manga in Your Language**: Enjoy manga that hasn't been officially translated yet, or prefer reading in your native language for better understanding.

🌍 **Support for 25+ Languages**: Translate between major languages including Japanese, English, Chinese (Simplified & Traditional), Korean, Spanish, French, German, and many more.

🎯 **Smart and Accurate**: Uses advanced artificial intelligence to understand context and provide natural-sounding translations that preserve the original meaning and tone.

📚 **Flexible for Any Project Size**: Whether you need to translate a single page, an entire book, or multiple books at once, there's a workflow designed for your needs.

⚡ **Fast Processing**: Takes advantage of your computer's graphics card (if available) to speed up the translation process dramatically.

🎨 **Preserves Original Artwork**: The translated text appears naturally integrated into the original images, maintaining the visual style and layout.

## What Can You Translate?

The tool works with common manga file formats:
- **Single images**: JPEG, PNG, GIF, BMP, TIFF, WebP
- **Manga books**: CBZ, CBR, EPUB, PDF files

## Available Tools and How They Work Together

### Core Building Blocks

#### 1. Translate Manga Page
Handles individual manga page images - perfect when you need to translate just one or a few pages.

**What it does:**
- Takes a single manga image
- Identifies and reads the text
- Translates it to your target language
- Returns the translated image in the same format

**Best for:**
- Testing translation quality before processing full books
- Translating standalone images or artwork
- Quick translations of specific pages

#### 2. Translate Manga Images
Processes multiple manga page images at once and saves them to a folder.

**What it does:**
- Accepts a collection of manga page images
- Translates all pages in sequence
- Organizes all translated images into a folder
- Maintains the original page order

**Best for:**
- Translating loose collections of manga pages
- Processing chapters that aren't in archive format
- When you want individual image files as output

### Complete Workflows

#### 3. Translate Manga Book
Transforms entire manga books from archive formats (CBZ, CBR, EPUB, PDF) into translated versions.

**What it does:**
- Opens manga book files (CBZ, CBR, EPUB, PDF)
- Extracts all pages
- Translates each page
- Repackages everything into a translated book file
- Preserves metadata like title and author

**Best for:**
- Translating complete manga volumes or chapters
- Converting your manga library to another language
- Maintaining book format for easy reading

**How it combines the building blocks:**
This workflow uses "Translate Manga Images" internally, but adds the ability to open archive files at the start and repackage them at the end. It's like a complete assembly line from raw book to finished translated book.

#### 4. Translate Manga Books (Batch)
Handles large-scale translation projects by processing an entire folder of manga books automatically.

**What it does:**
- Scans a folder for all manga book files
- Translates each book one after another
- Saves all translated books to your chosen location
- You can select which file formats to process (PDF, CBZ, CBR, EPUB)

**Best for:**
- Translating entire manga series at once
- Processing your complete manga collection
- Large-scale translation projects

**How it combines the building blocks:**
Think of this as running "Translate Manga Book" multiple times automatically. It searches your folder, creates a list of books to translate, and then processes each one. It's perfect when you have dozens or hundreds of books to translate.

### Combining Tools for Different Needs

**For Quick Tests:**
Start with "Translate Manga Page" to test one image and verify the translation quality meets your expectations.

**For Individual Books:**
Use "Translate Manga Book" when you have one or a few specific books to translate. It handles everything from opening to saving.

**For Large Libraries:**
Use "Translate Manga Books (Batch)" to process your entire collection. You might want to test with "Translate Manga Page" first to choose the best settings, then apply those settings to the batch workflow.

**For Loose Pages:**
If you have manga pages as separate image files (not in a book archive), use "Translate Manga Images" to process them all and get organized output.

## Supported Languages

### You Can Translate From:
- **Auto-detect** (automatically identifies the source language)
- Japanese (日本語)
- Chinese Simplified (简体中文)
- Chinese Traditional (繁體中文)
- Korean (한국어)
- English
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Italian (Italiano)
- Portuguese (Português)
- Russian (Русский)
- Arabic (العربية)
- Thai (ไทย)
- Vietnamese (Tiếng Việt)
- And 11 more languages

### You Can Translate To:
All of the above languages except auto-detect (you need to specify your target language).

## How to Get Started

### First-Time Setup
1. **Initial Download**: The first time you run a translation, the system will automatically download the necessary AI models. This is a one-time process that may take a few minutes depending on your internet speed.
2. **Check Your Hardware**: The tool will automatically use your graphics card (GPU) if available for faster processing. If not, it will use your computer's processor (CPU) - both work fine, GPU is just faster.

### Translating Your First Manga

#### For a Single Page:
1. Open the "Translate Single Manga Page" workflow
2. Upload your manga page image
3. Select your target language (the language you want)
4. Optionally choose the source language, or leave it on "auto" for automatic detection
5. Run the workflow
6. View or download your translated image

#### For a Manga Book:
1. Open the "Translate Manga Book" workflow
2. Select your manga book file (CBZ, CBR, EPUB, or PDF)
3. Choose where to save the translated book
4. Select your target language
5. Adjust settings if needed (they work great at default values)
6. Run the workflow
7. Your translated book will be ready to read

#### For Multiple Books:
1. Open the "Translate Manga Books (Batch)" workflow
2. Select the folder containing your manga books
3. Choose a folder where translated books will be saved
4. Select which file formats to process
5. Select your target language
6. Run the workflow and let it process all your books

### Understanding the Settings

**Target Language** (Required): The language you want your manga translated into.

**Source Language** (Optional): The original language of your manga. Setting this to "auto" lets the system detect it automatically, which works well in most cases.

**Hardware Acceleration** (Advanced):
- **CUDA**: Uses your graphics card for faster processing (if you have a compatible NVIDIA GPU)
- **CPU**: Uses your computer's processor (works everywhere, but slower)

**Model** (Advanced): The AI translation model used. The default settings provide excellent results for manga translation.

## Tips for Best Results

### Image Quality Matters
- **Higher resolution images** produce more accurate text recognition
- **Clear, crisp text** translates better than blurry or low-quality scans
- **Standard layouts** work better than highly stylized or artistic text

### Language Combinations
- **Popular pairs** like Japanese-to-English, Chinese-to-English, and Korean-to-English typically provide the best results since these are common translation directions
- **Direct translations** between two non-English languages may vary in quality depending on the language pair

### Batch Processing Tips
- **Test first**: Use the single page translator on a few pages to find your preferred settings before running large batches
- **Organize your files**: Keep manga books in separate folders by series or language for easier batch processing
- **Check disk space**: Make sure you have enough storage for both original and translated files

## Who Benefits from This Tool?

**Manga Readers**: Access manga in languages you understand, including content that hasn't been officially translated.

**Language Learners**: Compare original and translated versions to study Japanese, Chinese, Korean, or other languages.

**Content Creators**: Quickly create translated versions of manga for different audiences or regions.

**Publishers and Translators**: Speed up the initial translation process, though professional review is still recommended for publication.

**Accessibility Advocates**: Make manga content available to readers who speak different languages.

**Fan Communities**: Share manga with international fan bases by providing translations in multiple languages.

## What to Expect

### Processing Time
- **Single pages**: Usually complete in 10-30 seconds
- **Full books**: Depends on page count, typically 5-15 minutes for a standard volume
- **Batch processing**: Plan for several hours if translating large collections
- **GPU vs CPU**: Graphics card processing can be 3-5 times faster than processor-only

### Translation Quality
The quality of translations depends on several factors:
- **Text clarity**: Clean, well-defined text produces better results
- **Context complexity**: Simple dialogue translates more reliably than complex literary passages or wordplay
- **Language pair**: Some language combinations work better than others
- **Source material quality**: Better original scans lead to better translations

### Output Format
- **Preserves original format**: If you input a CBZ file, you get a CBZ file back
- **Special case**: CBR files are converted to CBZ format (both are comic book archives, CBZ is more widely supported)
- **Same quality**: Output images maintain the quality of the source material

## Privacy and How It Works

**Local Processing**: The text detection and image processing happen on your own computer. Your manga files stay with you.

**Cloud Translation**: The actual text translation uses OOMOL's secure translation service. Text content is sent securely over encrypted connections, translated, and the result is sent back. The service doesn't permanently store your content.

**Token Usage**: Translation services use OOMOL tokens from your account.

**No Data Collection**: Your manga files themselves are not stored on external servers. Only the extracted text is sent for translation.

## Technical Requirements

**Operating System**: Works on Windows, Mac, and Linux

**Internet Connection**: Required for downloading AI models (first time only) and accessing translation services

**Storage Space**:
- AI models require approximately 2-5 GB (one-time download)
- Ensure adequate space for both original and translated manga files

**Memory**: At least 4 GB RAM recommended, 8 GB or more for better performance

**Graphics Card** (Optional but Recommended):
- NVIDIA GPU with CUDA support for faster processing
- Not required - CPU processing works fine, just slower

## Common Questions

**Q: Can I translate manga in languages other than Japanese?**
A: Yes! The tool supports 25+ languages. You can translate Chinese, Korean, English, Spanish, French, and many other languages.

**Q: Will the translation be perfect?**
A: AI translation has improved dramatically but may not capture every nuance, especially with wordplay, cultural references, or artistic text. The results are very good for understanding and enjoyment, though professional human translation may still catch subtleties the AI misses.

**Q: Can I adjust the translation if something doesn't look right?**
A: The current version provides automated translation. For adjustments, you would need to edit the output images in an image editing program.

**Q: Do I need a powerful computer?**
A: Not necessarily. The tool works on regular computers using the CPU. A graphics card speeds things up but isn't required.

**Q: How much does it cost?**
A: The tool uses OOMOL tokens for translation services. Check your OOMOL account for token pricing and usage.

**Q: Can I use this for commercial purposes?**
A: Please respect copyright laws. Only translate manga you have the right to modify. This tool is designed for personal use and legitimate translation work.

---

## Getting Help

If you encounter issues or have questions:
- Check that you have enough disk space and memory available
- Verify your internet connection is stable
- Try translating a single page first to test your settings
- For technical support, visit the [project repository](https://github.com/oomol-flows/manga-translator)

---

*Built on the proven [manga-image-translator](https://github.com/zyddnys/manga-image-translator) technology and optimized for easy workflow-based processing.*

**Ready to explore manga in any language?** Load the workflow in your OOMOL platform and start your translation journey!
