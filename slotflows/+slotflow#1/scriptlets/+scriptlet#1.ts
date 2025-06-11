//#region generated meta
type Inputs = {
    args: any;
};
type Outputs = {
    pdf_file_path: string | null;
    device: "cuda" | "cpu";
    source_language: "auto" | "CHS" | "CHT" | "CSY" | "NLD" | "ENG" | "FRA" | "DEU" | "HUN" | "ITA" | "JPN" | "KOR" | "PLK" | "PTB" | "ROM" | "RUS" | "ESP" | "TRK" | "UKR" | "VIN" | "CNR" | "SRP" | "HRV" | "ARA" | "THA" | "IND";
    target_language: "CHS" | "CHT" | "CSY" | "NLD" | "ENG" | "FRA" | "DEU" | "HUN" | "ITA" | "JPN" | "KOR" | "PLK" | "PTB" | "ROM" | "RUS" | "ESP" | "TRK" | "UKR" | "VIN" | "CNR" | "SRP" | "HRV" | "ARA" | "THA" | "IND";
};
//#endregion

import type { Context } from "@oomol/types/oocana";

export default async function(
    params: Inputs,
    context: Context<Inputs, Outputs>
): Promise<Partial<Outputs> | undefined | void> {

    const {args} = params;

    return {
        pdf_file_path: args.pdf_file_path,
        device: args.device,
        source_language: args.source_language,
        target_language: args.target_language,
    };
};
