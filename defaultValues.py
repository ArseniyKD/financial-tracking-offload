DEFAULT_NEW_MONTH_INFO = [
    [ "Transaction Name", "Transaction Amount", "Transaction Date",
      "Transaction Category", "Budget Specifiers", "Transaction Note",
      "", "Aggregate", "", "", "FM Ceil", "Income", "Rents", "Spend" ],
    [ "" for _ in range( 10 ) ] + [ "1500", "", "2450", "=SUM(M2,K2,I20)" ],
    [ "" for _ in range( 7 ) ] + [ "Grocery",
                                   "=SUMIF($D$2:$D$200, H3, $B$2:$B$200)",
                                   "", "", "", "", "" ],
    [ "" for _ in range( 7 ) ] + [ "Bills",
                                   "=SUMIF($D$2:$D$200, H4, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Eating Out",
                                   "=SUMIF($D$2:$D$200, H5, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Retail",
                                   "=SUMIF($D$2:$D$200, H6, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Vices",
                                   "=SUMIF($D$2:$D$200, H7, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Health",
                                   "=SUMIF($D$2:$D$200, H8, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Subscriptions",
                                   "=SUMIF($D$2:$D$200, H9, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Transit",
                                   "=SUMIF($D$2:$D$200, H10, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Travel",
                                   "=SUMIF($D$2:$D$200, H11, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Entertainment",
                                   "=SUMIF($D$2:$D$200, H12, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Education",
                                   "=SUMIF($D$2:$D$200, H13, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Professional Services",
                                   "=SUMIF($D$2:$D$200, H14, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Other",
                                   "=SUMIF($D$2:$D$200, H15, $B$2:$B$200)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "Total",
                                   "=SUM(I3:I15)" ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 14 ) ],
    [ "" for _ in range( 14 ) ],
    [ "" for _ in range( 7 ) ] + [ "Reimbursed (rm)",
                                   '=SUMIF(E2:E200, "rm",B2:B200)' ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "spend - rm",
                                   '=I16-I19' ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "ws",
                                   '=SUMIF(E2:E200, "ws",B2:B200)' ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "spend - rm - ws",
                                   '=I20-I21' ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "extra",
                                   '=SUMIF(E2:E200, "extra",B2:B200)' ] + \
                                 [ "" for _ in range( 5 ) ],
    [ "" for _ in range( 7 ) ] + [ "spend - rm - ws - extra",
                                   '=I22-I23' ] + \
                                 [ "" for _ in range( 5 ) ]
]

DEFAULT_TRANSACTION_RANGE = "A:F"

DEFAULT_CATEGORY_SUMMARY_RANGE = "H3:I16"
DEFAULT_AGGREGATE_SUMMARY_RANGE = "H19:I24"

PRE_2026_LEGACY_CATEGORY_SUMMARY_RANGE = "H3:I13"
PRE_2026_LEGACY_AGGREGATE_SUMMARY_RANGE = "H16:I22"
