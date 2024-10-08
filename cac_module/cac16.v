
// Generated by Cadence Encounter(R) RTL Compiler v12.10-s012_1

// Verification Directory fv/CAC 

module CAC(PPI, K, OPO, LPO);
  input [15:0] PPI, K;
  input OPO;
  output LPO;
  wire [15:0] PPI, K;
  wire OPO;
  wire LPO;
  wire n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7;
  wire n_8, n_9, n_10, n_11, n_12, n_13, n_14, n_15;
  wire n_16, n_17, n_18, n_19, n_20, n_21, n_22, n_23;
  wire n_24, n_25, n_26, n_27, n_28, n_29, n_30, n_31;
  wire n_32, n_33, n_34, n_35, n_36, n_37, n_38, n_39;
  wire n_40, n_41, n_42, n_43, n_44, n_45, n_46, n_47;
  wire n_48, n_49;
  XOR2_X1 g1112(.A (n_48), .B (n_49), .Z (LPO));
  XNOR2_X1 g1113(.A (n_47), .B (OPO), .ZN (n_49));
  NOR2_X1 g1114(.A1 (n_47), .A2 (n_45), .ZN (n_48));
  NOR3_X1 g1115(.A1 (n_46), .A2 (PPI[0]), .A3 (PPI[1]), .ZN (n_47));
  NAND4_X1 g1116(.A1 (n_44), .A2 (n_26), .A3 (PPI[5]), .A4 (PPI[2]),
       .ZN (n_46));
  NOR4_X1 g1119(.A1 (n_39), .A2 (n_42), .A3 (n_43), .A4 (n_41), .ZN
       (n_45));
  NOR3_X1 g1117(.A1 (n_40), .A2 (PPI[6]), .A3 (PPI[8]), .ZN (n_44));
  NAND4_X1 g1124(.A1 (n_37), .A2 (n_29), .A3 (n_27), .A4 (n_28), .ZN
       (n_43));
  NAND4_X1 g1121(.A1 (n_36), .A2 (n_32), .A3 (n_19), .A4 (n_11), .ZN
       (n_42));
  NAND4_X1 g1122(.A1 (n_35), .A2 (n_3), .A3 (n_18), .A4 (n_12), .ZN
       (n_41));
  NAND3_X1 g1118(.A1 (n_38), .A2 (PPI[9]), .A3 (PPI[10]), .ZN (n_40));
  NAND4_X1 g1123(.A1 (n_34), .A2 (n_2), .A3 (n_9), .A4 (n_21), .ZN
       (n_39));
  NOR4_X1 g1120(.A1 (n_33), .A2 (n_8), .A3 (PPI[13]), .A4 (PPI[12]),
       .ZN (n_38));
  NOR3_X1 g1126(.A1 (n_4), .A2 (n_25), .A3 (n_24), .ZN (n_37));
  NOR3_X1 g1127(.A1 (n_1), .A2 (n_16), .A3 (n_20), .ZN (n_36));
  NOR3_X1 g1128(.A1 (n_0), .A2 (n_22), .A3 (n_6), .ZN (n_35));
  NOR3_X1 g1129(.A1 (n_30), .A2 (n_7), .A3 (n_14), .ZN (n_34));
  NAND4_X1 g1125(.A1 (n_31), .A2 (PPI[7]), .A3 (PPI[15]), .A4 (PPI[3]),
       .ZN (n_33));
  XOR2_X1 g1131(.A (K[11]), .B (n_31), .Z (n_32));
  XOR2_X1 g1136(.A (PPI[12]), .B (K[12]), .Z (n_30));
  XNOR2_X1 g1137(.A (PPI[7]), .B (K[7]), .ZN (n_29));
  NAND2_X1 g1138(.A1 (n_23), .A2 (PPI[6]), .ZN (n_28));
  OR2_X1 g1139(.A1 (n_26), .A2 (K[4]), .ZN (n_27));
  AND2_X1 g1140(.A1 (n_26), .A2 (K[4]), .ZN (n_25));
  NOR2_X1 g1141(.A1 (n_23), .A2 (PPI[6]), .ZN (n_24));
  NOR2_X1 g1142(.A1 (n_17), .A2 (PPI[0]), .ZN (n_22));
  NAND2_X1 g1143(.A1 (n_13), .A2 (PPI[13]), .ZN (n_21));
  NOR2_X1 g1144(.A1 (n_10), .A2 (PPI[8]), .ZN (n_20));
  NAND2_X1 g1145(.A1 (n_15), .A2 (PPI[10]), .ZN (n_19));
  NAND2_X1 g1146(.A1 (n_17), .A2 (PPI[0]), .ZN (n_18));
  NOR2_X1 g1147(.A1 (n_15), .A2 (PPI[10]), .ZN (n_16));
  NOR2_X1 g1148(.A1 (n_13), .A2 (PPI[13]), .ZN (n_14));
  NAND2_X1 g1149(.A1 (n_5), .A2 (PPI[2]), .ZN (n_12));
  NAND2_X1 g1150(.A1 (n_10), .A2 (PPI[8]), .ZN (n_11));
  OR2_X1 g1151(.A1 (n_8), .A2 (K[14]), .ZN (n_9));
  AND2_X1 g1152(.A1 (n_8), .A2 (K[14]), .ZN (n_7));
  NOR2_X1 g1153(.A1 (n_5), .A2 (PPI[2]), .ZN (n_6));
  XOR2_X1 g1130(.A (PPI[5]), .B (K[5]), .Z (n_4));
  XNOR2_X1 g1132(.A (PPI[3]), .B (K[3]), .ZN (n_3));
  XNOR2_X1 g1133(.A (PPI[15]), .B (K[15]), .ZN (n_2));
  XOR2_X1 g1134(.A (PPI[9]), .B (K[9]), .Z (n_1));
  XOR2_X1 g1135(.A (PPI[1]), .B (K[1]), .Z (n_0));
  INV_X1 g1159(.A (K[6]), .ZN (n_23));
  INV_X1 g1161(.A (K[10]), .ZN (n_15));
  INV_X1 g1154(.A (PPI[4]), .ZN (n_26));
  INV_X1 g1155(.A (K[0]), .ZN (n_17));
  INV_X1 g1160(.A (K[13]), .ZN (n_13));
  INV_X1 g1156(.A (PPI[11]), .ZN (n_31));
  INV_X1 g1157(.A (PPI[14]), .ZN (n_8));
  INV_X1 g1162(.A (K[8]), .ZN (n_10));
  INV_X1 g1158(.A (K[2]), .ZN (n_5));
endmodule

