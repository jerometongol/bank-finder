{ 
  "nbformat": 4, 
  "nbformat_minor": 0, 
  "metadata": { 
    "colab": { 
      "provenance": [] 
    }, 
    "kernelspec": { 
      "name": "python3", 
      "display_name": "Python 3" 
    }, 
    "language_info": { 
      "name": "python" 
    } 
  }, 
  "cells": [ 
    { 
      "cell_type": "code", 
      "execution_count": null, 
      "metadata": { 
        "id": "JB9lbsGxfpqq" 
      }, 
      "outputs": [], 
      "source": [ 
        "#Funding" 
      ] 
    }, 
    { 
      "cell_type": "code", 
      "source": [ 
        "import requests\n", 
        "import pandas as pd\n", 
        "from datetime import datetime\n", 
        "\n", 
        "def generate_bank_intelligence_report(state_code):\n", 
        "    state_code = state_code.upper()\n", 
        "    print(f\"--- BANKS FINDER: {state_code} ---\")\n", 
        "    print(f\"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\")\n", 
        "    print(\"=\"*150 + \"\\n\")\n", 
        "\n", 
        "    # 1. API CALL - Accurate accounting data (FDIC)\n", 
        "    fdic_url = \"https://banks.data.fdic.gov/api/financials\"\n", 
        "    params = {\n", 
        "        'filters': f'STALP:\"{state_code}\" AND ACTIVE:1',\n", 
        "        'fields': 'NAME,CITY,STALP,ASSET,DEP,LNLS,LNLSNET,REPDTE',\n", 
        "        'sort_by': 'REPDTE', 'sort_order': 'DESC', 'limit': 1000, 'format': 'json'\n", 
        "    }\n", 
        "\n", 
        "    try:\n", 
        "        response = requests.get(fdic_url, params=params)\n", 
        "        data = response.json().get('data', [])\n", 
        "        if not data: return f\"No baseline data found for {state_code}.\"\n", 
        "        df = pd.DataFrame([x['data'] for x in data])\n", 
        "        df['DEP'] = pd.to_numeric(df.get('DEP', 0), errors='coerce').fillna(0)\n", 
        "        df['ASSET'] = pd.to_numeric(df.get('ASSET', 0), errors='coerce').fillna(0)\n", 
        "        df['LOANS_VAL'] = pd.to_numeric(df.get('LNLSNET', 0), 
errors='coerce').fillna(pd.to_numeric(df.get('LNLS', 0), errors='coerce')).fillna(0)\n", 
        "        df['LDR'] = (df['LOANS_VAL'] / df['DEP'].replace(0, 1)) * 100\n", 
        "        df['NAME_UPPER'] = df['NAME'].str.upper()\n", 
        "        df_active = df[df['ASSET'] > 10000].drop_duplicates(subset=['NAME'])\n", 
        "    except Exception as e:\n", 
        "        return f\"Data processing error: {e}\"\n", 
        "\n", 
        "    # MASTER DATA SECTION I ---\n", 
        "    presence_db = {\n", 
        "        \"CHASE\": 
[\"AL\",\"AZ\",\"AR\",\"CA\",\"CO\",\"CT\",\"DE\",\"FL\",\"GA\",\"ID\",\"IL\",\"IN\",\"IA\",\"KS\",\"KY\",\
"LA\",\"ME\",\"MD\",\"MA\",\"MI\",\"MN\",\"MS\",\"MO\",\"MT\",\"NE\",\"NV\",\"NH\",\"NJ\",\"NM\",\"
NY\",\"NC\",\"ND\",\"OH\",\"OK\",\"OR\",\"PA\",\"RI\",\"SC\",\"SD\",\"TN\",\"TX\",\"UT\",\"VT\",\"VA\"
,\"WA\",\"WV\",\"WI\",\"WY\",\"DC\"],\n", 
        "        \"AMEX\": [\"ALL\"], \"TRUIST\": 
[\"AL\",\"AR\",\"FL\",\"GA\",\"IN\",\"KY\",\"MD\",\"MS\",\"NJ\",\"NC\",\"OH\",\"PA\",\"SC\",\"TN\",\"TX
\",\"VA\",\"WV\",\"DC\"],\n", 
        "        \"WELLS FARGO\": 
[\"AL\",\"AK\",\"AZ\",\"AR\",\"CA\",\"CO\",\"CT\",\"DE\",\"FL\",\"GA\",\"ID\",\"IL\",\"IN\",\"IA\",\"KS\",\
"KY\",\"MT\",\"NE\",\"NV\",\"NJ\",\"NM\",\"NY\",\"NC\",\"ND\",\"OH\",\"OR\",\"PA\",\"SC\",\"SD\",\"T
N\",\"TX\",\"UT\",\"VA\",\"WA\",\"WI\",\"WY\",\"DC\"],\n", 
        "        \"CITIZENS\": 
[\"CT\",\"DE\",\"FL\",\"MD\",\"MA\",\"MI\",\"NH\",\"NJ\",\"NY\",\"OH\",\"PA\",\"RI\",\"VT\",\"VA\",\"DC
\"],\n", 
        "        \"FIRST CITIZENS\": 
[\"AZ\",\"CA\",\"CO\",\"FL\",\"GA\",\"KS\",\"MD\",\"MO\",\"NE\",\"NV\",\"NM\",\"NC\",\"OK\",\"OR\",\"
SC\",\"TN\",\"TX\",\"VA\",\"WA\",\"WV\",\"WI\"],\n", 
        "        \"5/3RD BANK\": 
[\"AL\",\"FL\",\"GA\",\"IL\",\"IN\",\"KY\",\"MI\",\"NC\",\"OH\",\"SC\",\"TN\",\"WV\"],\n", 
        "        \"BANK OF AMERICA\": 
[\"AL\",\"AZ\",\"AR\",\"CA\",\"CO\",\"CT\",\"DE\",\"FL\",\"GA\",\"ID\",\"IL\",\"IN\",\"IA\",\"KS\",\"KY\",\
"LA\",\"ME\",\"MD\",\"MA\",\"MI\",\"MN\",\"MO\",\"NE\",\"NV\",\"NH\",\"NJ\",\"NM\",\"NY\",\"NC\",\"
OH\",\"OK\",\"OR\",\"PA\",\"RI\",\"SC\",\"TN\",\"TX\",\"UT\",\"VA\",\"WA\",\"WI\",\"DC\"],\n", 
        "        \"US BANK\": 
[\"AZ\",\"AR\",\"CA\",\"CO\",\"FL\",\"ID\",\"IL\",\"IN\",\"IA\",\"KS\",\"KY\",\"MN\",\"MO\",\"MT\",\"NE\"
,\"NV\",\"NM\",\"NC\",\"ND\",\"OH\",\"OR\",\"SD\",\"TN\",\"UT\",\"WA\",\"WI\",\"WY\"],\n", 
        "        \"PNC\": 
[\"AL\",\"AZ\",\"CA\",\"CO\",\"DE\",\"FL\",\"GA\",\"IL\",\"IN\",\"KS\",\"KY\",\"MD\",\"MA\",\"MI\",\"MO\
",\"NJ\",\"NM\",\"NY\",\"NC\",\"OH\",\"PA\",\"SC\",\"TN\",\"TX\",\"VA\",\"WV\",\"DC\"]\n", 
        "    }\n", 
        "\n", 
        "    master_issuers = [\n", 
        "        {\"Key\": \"CHASE\", \"Disp\": \"CHASE\", \"Prod\": \"Ink Business Cash\", \"APR_0\": 
\"12 Mo 0%\", \"Bur\": \"EX\"},\n", 
        "        {\"Key\": \"AMEX\", \"Disp\": \"AMEX\", \"Prod\": \"Blue Business Plus\", \"APR_0\": 
\"12 Mo 0%\", \"Bur\": \"EX\"},\n", 
        "        {\"Key\": \"TRUIST\", \"Disp\": \"TRUIST\", \"Prod\": \"Enjoy Business Cash\", 
\"APR_0\": \"12 Mo 0%\", \"Bur\": \"EQ\"},\n", 
        "        {\"Key\": \"WELLS FARGO\", \"Disp\": \"WELLS FARGO\", \"Prod\": \"Signify 
Business\", \"APR_0\": \"12 Mo 0%\", \"Bur\": \"EX\"},\n", 
        "        {\"Key\": \"CITIZENS\", \"Disp\": \"CITIZENS\", \"Prod\": \"Biz Platinum\", \"APR_0\": 
\"12 Mo 0%\", \"Bur\": \"EX-EQ\"},\n", 
        "        {\"Key\": \"FIRST CITIZENS\", \"Disp\": \"FIRST CITIZENS\", \"Prod\": \"Biz Great 
Rewards\", \"APR_0\": \"9 Mo 0%\", \"Bur\": \"EX\"},\n", 
        "        {\"Key\": \"5/3RD BANK\", \"Disp\": \"5/3RD BANK\", \"Prod\": \"Business Standard\", 
\"APR_0\": \"12 Mo 0%\", \"Bur\": \"EX\"},\n", 
        "        {\"Key\": \"BANK OF AMERICA\", \"Disp\": \"BANK OF AMERICA\", \"Prod\": 
\"Advantage Custom\", \"APR_0\": \"9 Mo 0%\", \"Bur\": \"EX-TU\"},\n", 
        "        {\"Key\": \"US BANK\", \"Disp\": \"US BANK\", \"Prod\": \"Triple Cash Biz\", \"APR_0\": 
\"15 Mo 0%\", \"Bur\": \"EX\"},\n", 
        "        {\"Key\": \"PNC\", \"Disp\": \"PNC\", \"Prod\": \"PNC Visa Business\", \"APR_0\": \"13 
Mo 0%\", \"Bur\": \"EX/Soft EQ\"}\n", 
        "    ]\n", 
        "\n", 
        "    sec2_names, sec3_names, sec5_names = [], [], []\n", 
        "\n", 
        "    # I. DIRECT NATIONAL ISSUERS\n", 
        "    print(f\"I. DIRECT NATIONAL ISSUERS WITH BRANCH PRESENCE & 0% APR IN 
{state_code}\")\n", 
        "    print(f\"{'Bank'.ljust(18)} | {'Top 0% APR Product'.ljust(30)} | {'Intro 0% APR'.ljust(12)} | 
{'Bureau'.ljust(10)} | Online App\")\n", 
        "    print(\"-\" * 115)\n", 
        "    for b in master_issuers:\n", 
        "        if state_code in presence_db.get(b['Key'], []) or \"ALL\" in presence_db.get(b['Key'], 
[]):\n", 
        "            print(f\"{b['Disp'].ljust(18)} | {b['Prod'].ljust(30)} | {b['APR_0'].ljust(12)} | 
{b['Bur'].ljust(10)} | YES (Direct)\")\n", 
        "\n", 
        "    # II. ELAN PARTNERS\n", 
        "    print(\"\\n\" + \"-\"*150 + f\"\\nII. PROBABLE ELAN CARD ASSET PARTNERS 
(REGIONAL NETWORK) - {state_code}\")\n", 
        "    print(f\"{'Bank Name'.ljust(45)} | {'Intro 0% APR'.ljust(15)} | {'Online App'.ljust(15)} | 
{'Target Bureau'}\")\n", 
        "    print(\"-\" * 115)\n", 
        "    elan_df = df_active[df_active['ASSET'] >= 1000000].sort_values('ASSET', 
ascending=False).head(15)\n", 
        "    for _, row in elan_df.iterrows():\n", 
        "        if not any(iss['Key'] in row['NAME_UPPER'] for iss in master_issuers):\n", 
        "            sec2_names.append(row['NAME'])\n", 
        "            print(f\" - {row['NAME'].ljust(43)} | {'12-15 Mo 0%'.ljust(15)} | {'YES 
(Direct)'.ljust(15)} | TU (Typical)\")\n", 
        "\n", 
        "    # III. TCM PARTNERS\n", 
        "    print(\"\\n\" + \"-\"*150 + f\"\\nIII. PROBABLE TCM BANK PARTNERS (COMMUNITY 
NETWORK) - {state_code}\")\n", 
        "    print(f\"{'Bank Name'.ljust(45)} | {'Intro 0% APR'.ljust(15)} | {'Online App'.ljust(15)} | 
{'Target Bureau'}\")\n", 
        "    print(\"-\" * 115)\n", 
        "    tcm_df = df_active[(df_active['ASSET'] < 1000000) & (df_active['ASSET'] >= 
50000)].sort_values('ASSET', ascending=False).head(20)\n", 
        "    for _, row in tcm_df.iterrows():\n", 
        "        sec3_names.append(row['NAME'])\n", 
        "        online_status = \"YES (Direct)\" if row['ASSET'] > 250000 else \"YES (Lead 
Form)\"\n", 
        "        print(f\" - {row['NAME'].ljust(43)} | {'6-12 Mo 0%'.ljust(15)} | {online_status.ljust(15)} | 
EX (Typical)\")\n", 
        "\n", 
        "    # IV. GENERAL INDEPENDENT ISSUERS\n", 
        "    print(\"\\n\" + \"-\"*150 + f\"\\nIV. GENERAL INDEPENDENT ISSUERS (NON-ELAN / 
NON-TCM / NON-SEC I) - {state_code}\")\n", 
        "    print(f\"{'Bank Name'.ljust(45)} | {'Status'.ljust(25)} | {'Intro 0% APR'.ljust(15)} | Online 
App\")\n", 
        "    print(\"-\" * 115)\n", 
        "    all_prev_keys = [iss['Key'] for iss in master_issuers]\n", 
        "    sec5_candidates = df_active[~df_active['NAME'].isin(sec2_names + sec3_names) &\n", 
        "                                ~df_active['NAME_UPPER'].str.contains('|'.join(all_prev_keys))]\n", 
        "    sec5_list = sec5_candidates.sort_values('ASSET', ascending=False).head(15)\n", 
        "    for _, row in sec5_list.iterrows():\n", 
        "        sec5_names.append(row['NAME'])\n", 
        "        print(f\" - {row['NAME'].ljust(43)} | {'Direct/Indep. Issuer'.ljust(25)} | {'9-12 Mo 
0%'.ljust(15)} | Check Site\")\n", 
        "\n", 
        "    # V. HIGH LIQUIDITY ANALYSIS\n", 
        "    print(\"\\n\" + \"-\"*150 + \"\\nV. HIGH LIQUIDITY ANALYSIS (TARGET: LOW CD RATES 
0% - 2%)\")\n", 
        "    high_liq = df_active[(df_active['LDR'] < 75) & (df_active['LDR'] > 
5)].sort_values('LDR').head(25).copy()\n", 
        "    def est_rate(ldr): return \"Lowest (0.1%-1.0%)\" if ldr < 50 else \"Low (1.1%-2.0%)\"\n", 
        "    high_liq['CD Rate Est.'] = high_liq['LDR'].apply(est_rate)\n", 
        "    print(high_liq[['NAME', 'LDR', 'CITY', 'CD Rate Est.']].rename(columns={'NAME': 'Bank 
Name', 'LDR': 'LDR %'}).to_string(index=False))\n", 
        "\n", 
        "    # VI. TOP STRATEGIC TARGETS\n", 
        "    print(\"\\n\" + \"=\"*150)\n", 
        "    print(f\"VI. TOP STRATEGIC TARGETS (HIGH LIQUIDITY + CONFIRMED CREDIT 
PRODUCTS)\")\n", 
        "    print(f\"{'Bank Name'.ljust(45)} | {'LDR %'.ljust(10)} | {'CD Rate Est.'.ljust(20)} | {'Origin 
Section'}\")\n", 
        "    print(\"-\" * 115)\n", 
        "\n", 
        "    match_found = False\n", 
        "    for _, row in high_liq.iterrows():\n", 
        "        origin = \"\"\n", 
        "        if row['NAME'] in sec2_names: origin = \"Sec II (Elan Partner)\"\n", 
        "        elif row['NAME'] in sec3_names: origin = \"Sec III (TCM Partner)\"\n", 
        "        elif row['NAME'] in sec5_names: origin = \"Sec IV (Independent)\"\n", 
        "\n", 
        "        if origin:\n", 
        "            print(f\" - {row['NAME'].ljust(43)} | {str(round(row['LDR'],2)).ljust(10)} | {row['CD 
Rate Est.'].ljust(20)} | {origin}\")\n", 
        "            match_found = True\n", 
        "\n", 
        "    if not match_found:\n", 
        "        print(\"No exact matches found in the top liquidity scan. Expand search parameters 
for more results.\")\n", 
        "\n", 
        "# EXECUTION\n", 
        "generate_bank_intelligence_report(\"FL\")" 
      ], 
      "metadata": { 
        "colab": { 
          "base_uri": "https://localhost:8080/" 
        }, 
        "id": "9QwjXObZmzBm", 
        "outputId": "560c1f3c-4008-49f7-a23d-001a2be722d1" 
      }, 
      "execution_count": 3, 
      "outputs": [ 
        { 
          "output_type": "stream", 
          "name": "stdout", 
          "text": [ 
            "--- BANKS FINDER: FL ---\n", 
            "Generated on: 2026-04-28 21:07\n", 
            
"========================================================================
========================================================================
======\n", 
            "\n", 
            "I. DIRECT NATIONAL ISSUERS WITH BRANCH PRESENCE & 0% APR IN FL\n", 
            "Bank               | Top 0% APR Product             | Intro 0% APR | Bureau     | Online 
App\n", 
            
"-------------------------------------------------------------------------------------------------------------------\n", 
            "CHASE              | Ink Business Cash              | 12 Mo 0%     | EX         | YES (Direct)\n", 
            "AMEX               | Blue Business Plus             | 12 Mo 0%     | EX         | YES (Direct)\n", 
            "TRUIST             | Enjoy Business Cash            | 12 Mo 0%     | EQ         | YES 
(Direct)\n", 
            "WELLS FARGO        | Signify Business               | 12 Mo 0%     | EX         | YES 
(Direct)\n", 
            "CITIZENS           | Biz Platinum                   | 12 Mo 0%     | EX-EQ      | YES (Direct)\n", 
            "FIRST CITIZENS     | Biz Great Rewards              | 9 Mo 0%      | EX         | YES 
(Direct)\n", 
            "5/3RD BANK         | Business Standard              | 12 Mo 0%     | EX         | YES 
(Direct)\n", 
            "BANK OF AMERICA    | Advantage Custom               | 9 Mo 0%      | EX-TU      | YES 
(Direct)\n", 
            "US BANK            | Triple Cash Biz                | 15 Mo 0%     | EX         | YES (Direct)\n", 
            "PNC                | PNC Visa Business              | 13 Mo 0%     | EX/Soft EQ | YES 
(Direct)\n", 
            "\n", 
            
"------------------------------------------------------------------------------------------------------------------------------------------------------\n", 
            "II. PROBABLE ELAN CARD ASSET PARTNERS (REGIONAL NETWORK) - FL\n", 
            "Bank Name                                     | Intro 0% APR    | Online App      | Target Bureau\n", 
            
"-------------------------------------------------------------------------------------------------------------------\n", 
            " - SOUTHSTATE BANK NA                          | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - EVERBANK NATIONAL ASSN                      | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - RAYMOND JAMES BANK                          | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - TIAA FSB                                    | 12-15 Mo 0%     | YES (Direct)    | TU (Typical)\n", 
            " - BANKUNITED NATIONAL ASSN                    | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - CITY NB OF FLORIDA                          | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - SEACOAST NATIONAL BANK                      | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - AMERANT BANK NATIONAL ASSN                  | 12-15 Mo 0%     | YES (Direct)    | 
TU (Typical)\n", 
            " - OCEAN BANK                                  | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - EMIGRANT BANK                               | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - BANESCO USA                                 | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - BRADESCO BANK                               | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - CAPITAL CITY BANK                           | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            " - FIRST FEDERAL BANK                          | 12-15 Mo 0%     | YES (Direct)    | TU 
(Typical)\n", 
            "\n", 
            
"------------------------------------------------------------------------------------------------------------------------------------------------------\n", 
            "III. PROBABLE TCM BANK PARTNERS (COMMUNITY NETWORK) - FL\n", 
            "Bank Name                                     | Intro 0% APR    | Online App      | Target Bureau\n", 
            
"-------------------------------------------------------------------------------------------------------------------\n", 
            " - PRIME MERIDIAN BANK                         | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - MAINSTREET CMTY BANK OF FL                  | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - WAUCHULA STATE BANK                         | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - TERRABANK NATIONAL ASSN                     | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - UNITED SOUTHERN BANK                        | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - WINTER PARK NATIONAL BANK                   | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - FIRST BANK                                  | 6-12 Mo 0%      | YES (Direct)    | EX (Typical)\n", 
            " - HEARTLAND NATIONAL BANK                     | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - AXIOM BANK NATIONAL ASSN                    | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - FLAGSHIP BANK                               | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - MARINE BANK&TRUST CO                        | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - FLORIDA CAPITAL BANK NA                     | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - FNBT BANK                                   | 6-12 Mo 0%      | YES (Direct)    | EX (Typical)\n", 
            " - CHARLOTTE STATE BANK&TRUST                  | 6-12 Mo 0%      | YES (Direct)    | 
EX (Typical)\n", 
            " - SUNRISE BANK                                | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - ANCHOR BANK                                 | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - SUNSTATE BANK                               | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - ENGLEWOOD BANK&TRUST                        | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - INTRACOASTAL BANK                           | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            " - FLAGLER BANK                                | 6-12 Mo 0%      | YES (Direct)    | EX 
(Typical)\n", 
            "\n", 
            
"------------------------------------------------------------------------------------------------------------------------------------------------------\n", 
            "IV. GENERAL INDEPENDENT ISSUERS (NON-ELAN / NON-TCM / NON-SEC I) - 
FL\n", 
            "Bank Name                                     | Status                    | Intro 0% APR    | Online 
App\n", 
            
"-------------------------------------------------------------------------------------------------------------------\n", 
            " - FINEMARK NATIONAL BANK&TRUST                | Direct/Indep. Issuer      | 9-12 Mo 
0%      | Check Site\n", 
            " - BANCO DO BRASIL AMERICAS                    | Direct/Indep. Issuer      | 9-12 Mo 0%      
| Check Site\n", 
            " - BANK OF TAMPA                               | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - U S CENTURY BANK                            | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - COGENT BANK                                 | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - CREWS BANK&TRUST                            | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - ONE FLORIDA BANK                            | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - NEWTEK BANK NATIONAL ASSN                   | Direct/Indep. Issuer      | 9-12 Mo 0%      
| Check Site\n", 
            " - CLIMATE FIRST BANK                          | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - INTERCREDIT BANK NA                         | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - INTERNATIONAL FINANCE BANK                  | Direct/Indep. Issuer      | 9-12 Mo 0%      
| Check Site\n", 
            " - PACIFIC NATIONAL BANK                       | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - GROVE BANK&TRUST                            | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - BAYFIRST NATIONAL BANK                      | Direct/Indep. Issuer      | 9-12 Mo 0%      | 
Check Site\n", 
            " - BANK OF CENTRAL FLORIDA                     | Direct/Indep. Issuer      | 9-12 Mo 0%      
| Check Site\n", 
            "\n", 
            
"------------------------------------------------------------------------------------------------------------------------------------------------------\n", 
            "V. HIGH LIQUIDITY ANALYSIS (TARGET: LOW CD RATES 0% - 2%)\n", 
            "                  Bank Name     LDR %             CITY       CD Rate Est.\n", 
            "    HEARTLAND NATIONAL BANK 22.422916          SEBRING Lowest (0.1%-1.0%)\n", 
            "COMMUNITY BANK OF THE SOUTH 30.701118   MERRITT ISLAND Lowest 
(0.1%-1.0%)\n", 
            "            WARRINGTON BANK 34.967286        PENSACOLA Lowest (0.1%-1.0%)\n", 
            "        CITIZENS FIRST BANK 36.561384     THE VILLAGES Lowest (0.1%-1.0%)\n", 
            "       COMMUNITY STATE BANK 37.344083           STARKE Lowest (0.1%-1.0%)\n", 
            "       ENGLEWOOD BANK&TRUST 37.810613        ENGLEWOOD Lowest 
(0.1%-1.0%)\n", 
            " PEOPLES BANK OF GRACEVILLE 38.533580       GRACEVILLE Lowest 
(0.1%-1.0%)\n", 
            " FIRST NB NORTHWEST FLORIDA 39.238224      PANAMA CITY Lowest 
(0.1%-1.0%)\n", 
            "       EDISON NATIONAL BANK 40.097387       FORT MYERS Lowest (0.1%-1.0%)\n", 
            " CHARLOTTE STATE BANK&TRUST 40.901353   PORT CHARLOTTE Lowest 
(0.1%-1.0%)\n", 
            "     FIRST NB OF MOUNT DORA 41.045952       MOUNT DORA Lowest 
(0.1%-1.0%)\n", 
            "         FIRST FEDERAL BANK 42.784861        LAKE CITY Lowest (0.1%-1.0%)\n", 
            "                   DLP BANK 44.554253           STARKE Lowest (0.1%-1.0%)\n", 
            "                  FNBT BANK 45.029531 FORT WALTON BEAC Lowest (0.1%-1.0%)\n", 
            "        BANK OF BELLE GLADE 45.450797      BELLE GLADE Lowest (0.1%-1.0%)\n", 
            "                  BANKMIAMI 46.043447     CORAL GABLES Lowest (0.1%-1.0%)\n", 
            "               BRANNEN BANK 49.700452        INVERNESS Lowest (0.1%-1.0%)\n", 
            "                SURETY BANK 53.354760           DELAND    Low (1.1%-2.0%)\n", 
            "     MADISON CNTY CMTY BANK 55.933844          MADISON    Low (1.1%-2.0%)\n", 
            "       UNITED SOUTHERN BANK 56.137373         UMATILLA    Low (1.1%-2.0%)\n", 
            "  WINTER PARK NATIONAL BANK 57.787142      WINTER PARK    Low 
(1.1%-2.0%)\n", 
            "          BANK OF PENSACOLA 58.065630        PENSACOLA    Low (1.1%-2.0%)\n", 
            "           CREWS BANK&TRUST 60.403237         WAUCHULA    Low (1.1%-2.0%)\n", 
            "        INTERCREDIT BANK NA 60.523792     CORAL GABLES    Low (1.1%-2.0%)\n", 
            "        CITIZENS BANK&TRUST 61.837122       FROSTPROOF    Low (1.1%-2.0%)\n", 
            "\n", 
            
"========================================================================
========================================================================
======\n", 
            "VI. TOP STRATEGIC TARGETS (HIGH LIQUIDITY + CONFIRMED CREDIT 
PRODUCTS)\n", 
            "Bank Name                                     | LDR %      | CD Rate Est.         | Origin Section\n", 
            
"-------------------------------------------------------------------------------------------------------------------\n", 
            " - HEARTLAND NATIONAL BANK                     | 22.42      | Lowest (0.1%-1.0%)   | Sec 
III (TCM Partner)\n", 
            " - ENGLEWOOD BANK&TRUST                        | 37.81      | Lowest (0.1%-1.0%)   | Sec 
III (TCM Partner)\n", 
            " - CHARLOTTE STATE BANK&TRUST                  | 40.9       | Lowest (0.1%-1.0%)   | 
Sec III (TCM Partner)\n", 
            " - FIRST FEDERAL BANK                          | 42.78      | Lowest (0.1%-1.0%)   | Sec II 
(Elan Partner)\n", 
            " - FNBT BANK                                   | 45.03      | Lowest (0.1%-1.0%)   | Sec III (TCM 
Partner)\n", 
            " - UNITED SOUTHERN BANK                        | 56.14      | Low (1.1%-2.0%)      | Sec III 
(TCM Partner)\n", 
            " - WINTER PARK NATIONAL BANK                   | 57.79      | Low (1.1%-2.0%)      | Sec 
III (TCM Partner)\n", 
            " - CREWS BANK&TRUST                            | 60.4       | Low (1.1%-2.0%)      | Sec IV 
(Independent)\n", 
            " - INTERCREDIT BANK NA                         | 60.52      | Low (1.1%-2.0%)      | Sec IV 
(Independent)\n" 
          ] 
        } 
      ] 
    } 
  ] 
} 
 
