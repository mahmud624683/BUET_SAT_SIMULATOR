module DFF(Q, clk, D);
input D;
input clk;
output Q;
always @(clk)
begin
  Q <= D;
end
endmodule


module c17_libar(G1gat,G2gat,G3gat,G6gat,G7gat,keyinput0,keyinput1,keyinput2,keyinput3,G22gat,G23gat);

input G1gat,G2gat,G3gat,G6gat,G7gat,keyinput0,keyinput1,keyinput2,keyinput3;
output G22gat,G23gat;
wire G10gat,G11gat,CLK2,LIBAR2,RLL2,G16gat,CLK1,LIBAR1,RLL1,RLL3,G19gat,RLL0;

nand NAND2_1 (G10gat, G1gat, G3gat);
nand NAND2_2 (G11gat, G3gat, G6gat);
nor NOR2_3 (CLK2, G11gat, G10gat);
dff DFF2_4 (LIBAR2, CLK2, keyinput2);
xor XOR2_5 (RLL2, G11gat, LIBAR2);
nand NAND2_6 (G16gat, G2gat, RLL2);
nor NOR2_7 (CLK1, G11gat, G16gat);
dff DFF2_8 (LIBAR1, CLK1, keyinput1);
xnor XNOR2_9 (RLL1, G11gat, LIBAR1);
xnor XNOR2_10 (RLL3, RLL1, keyinput3);
nand NAND2_11 (G19gat, RLL3, G7gat);
xor XOR2_12 (RLL0, G10gat, keyinput0);
nand NAND2_13 (G22gat, RLL0, G16gat);
nand NAND2_14 (G23gat, G16gat, G19gat);

endmodule