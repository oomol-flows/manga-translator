import os
import sys
sys.path.append(os.path.join(sys.path[0], '..', '..', 'manga-image-translator'))

from argparse import Namespace

from manga_translator import (
    set_main_logger, load_dictionary, apply_dictionary,
)
from manga_translator.utils import (
    get_logger,
    natural_sort,
)

# TODO: Dynamic imports to reduce ram usage in web(-server) mode. Will require dealing with args.py imports.

async def run(args: Namespace):
    logger = get_logger(args.mode)
    set_main_logger(logger)

    args_dict = vars(args)

    if args.mode == 'local':
        if not args.input:
            raise Exception('No input image was supplied. Use -i <image_path>')
        from manga_translator.mode.local import MangaTranslatorLocal
        translator = MangaTranslatorLocal(args_dict)

        # Load pre-translation and post-translation dictionaries
        pre_dict = load_dictionary(args.pre_dict)
        post_dict = load_dictionary(args.post_dict)

        if len(args.input) == 1 and os.path.isfile(args.input[0]):
            raise Exception('Need a directory for batch processing')

        else:
            dest = args.dest
            for path in natural_sort(args.input):
                    # Apply pre-translation dictionaries
                await translator.translate_path(path, dest, args_dict)
                for textline in translator.textlines:
                    textline.text = apply_dictionary(textline.text, pre_dict)
                    logger.info(f'Pre-translation dictionary applied: {textline.text}')

                    # Apply post-translation dictionaries
                for textline in translator.textlines:
                    textline.translation = apply_dictionary(textline.translation, post_dict)
                    logger.info(f'Post-translation dictionary applied: {textline.translation}')
