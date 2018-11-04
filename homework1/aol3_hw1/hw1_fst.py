from fst import *

# here are some predefined character sets that might come in handy.
# you can define your own
A2Z = set("abcdefghijklmnopqrstuvwxyz")
VOWS = set("aeiou")
CONS = set("bcdfghjklmnprstvwxyz")
AOIU = set("aoiu")
AOU = set("aou")
DLT = set("dlt")
E = set("e")
D = set("d")
I = set("i")
U = set("u")
N = set("n")
P = set("p")
T = set("t")
R = set("r")

# Implement your solution here
def buildFST1():
    print("Your task is to implement a better FST in the buildFST() function, using the methods described here")
    print("You may define additional methods in this module (hw1_fst.py) as desired")
    #
    # The states (you need to add more)
    # ---------------------------------------
    # 
    f = FST("q0") # q0 is the initial (non-accepting) state
    f.addState("q1") # a non-accepting state
    f.addState("q_ing") # a non-accepting state
    f.addState("q_EOW", True) # an accepting state (you shouldn't need any additional accepting states)

    #
    # The transitions (you need to add more):
    # ---------------------------------------
    # transduce every element in this set to itself: 
    f.addSetTransition("q0", A2Z, "q1")
    # AZ-E =  the set AZ without the elements in the set E
    f.addSetTransition("q1", A2Z-E, "q1")
    # get rid of this transition! (it overgenerates):
    #f.addSetTransition("q1", E, "q_ing")
    f.addTransition("q1","e","","q_ing")
    # map the empty string to ing: 
    f.addTransition("q_ing", "", "ing", "q_EOW")

    # Return your completed FST
    return f

def buildFST2():
    f = FST("q0")

    f.addState("q1_AOIU")
    f.addState("q1_E")
    f.addState("q1_U")
    f.addState("q1_Con")
    f.addState("q1_DLT")
    f.addState("q2_DLTI")
    f.addState("q2_DI") #Here if it receives an "e", then it automatically comes to end
    f.addState("Con_Vow")
    f.addState("Con_E")
    f.addState("U_E")
    f.addState("U_Vow")
    f.addState("Vow_Vow")
    f.addState("Vow_E")
    f.addState("Con_Con")
    f.addState("Con_U")
    f.addState("E_N")
    f.addState("Vow_N")
    f.addState("Vow_P")
    f.addState("Vow_T")
    f.addState("E_R")
    f.addState("Vow_R")
    f.addState("Vow_Con")
    f.addState("q_ing", False) # a non-accepting state
    f.addState("q_EOW", True) # an accepting state (you shouldn't need any additional accepting states)

    f.addSetTransition("q0",AOIU,"q1_AOIU")
    f.addSetTransition("q0",E,"q1_E")
    f.addSetTransition("q0",DLT,"q1_DLT") #last
    f.addSetTransition("q0",CONS-DLT,"q1_Con")

    f.addSetTransition("q1_AOIU",N,"Vow_N")
    f.addSetTransition("q1_AOIU",P,"Vow_P")
    f.addSetTransition("q1_AOIU",R,"Vow_R")
    f.addSetTransition("q1_AOIU",T,"Vow_T")
    f.addSetTransition("q1_AOIU",CONS-N-P-R-T,"Vow_Con")
    f.addSetTransition("q1_AOIU",VOWS - E,"Vow_Vow")
    f.addTransition("q1_AOIU","e","","Vow_Vow")

    f.addSetTransition("q1_DLT",AOU,"Con_Vow")
    f.addTransition("q1_DLT","e","","Con_E")
    f.addTransition("q1_DLT","i","","q2_DLTI")
    f.addSetTransition("q1_DLT",CONS,"Con_Con")


    f.addSetTransition("q1_E",N,"E_N")
    f.addSetTransition("q1_E",P,"Vow_P")
    f.addSetTransition("q1_E",T,"Vow_T")
    f.addSetTransition("q1_E",R,"E_R")
    f.addSetTransition("q1_E",CONS-N-P-R-T,"Vow_Con")
    f.addSetTransition("q1_E",VOWS - E,"Vow_Vow")
    f.addTransition("q1_E","e","","Vow_Vow")

    f.addSetTransition("q1_Con",VOWS - E  - U, "Con_Vow")
    f.addTransition("q1_Con","e","","Con_E")
    f.addSetTransition("q1_Con",U, "Con_U")
    f.addSetTransition("q1_Con",CONS,"Con_Con")

    f.addTransition("q2_DLTI", "a", "ia", "Vow_Vow")
    f.addTransition("q2_DLTI", "b", "ib", "Vow_Con")
    f.addTransition("q2_DLTI", "c", "ic", "Vow_Con")
    f.addTransition("q2_DLTI", "d", "id", "Vow_Con")
    f.addTransition("q2_DLTI", "e", "ying", "q_ing")
    f.addTransition("q2_DLTI", "f", "if", "Vow_Con")
    f.addTransition("q2_DLTI", "g", "ig", "Vow_Con")
    f.addTransition("q2_DLTI", "h", "ih", "Vow_Con")
    f.addTransition("q2_DLTI", "i", "ii", "Vow_Vow")
    f.addTransition("q2_DLTI", "j", "ij", "Vow_Con")
    f.addTransition("q2_DLTI", "k", "ik", "Vow_Con")
    f.addTransition("q2_DLTI", "l", "il", "Vow_Con")
    f.addTransition("q2_DLTI", "m", "im", "Vow_Con")
    f.addTransition("q2_DLTI", "n", "in", "Vow_N")
    f.addTransition("q2_DLTI", "o", "io", "Vow_Vow")
    f.addTransition("q2_DLTI", "p", "ip", "Vow_P")
    f.addTransition("q2_DLTI", "q", "iq", "Vow_Con")
    f.addTransition("q2_DLTI", "r", "ir", "Vow_R")
    f.addTransition("q2_DLTI", "s", "is", "Vow_Con")
    f.addTransition("q2_DLTI", "t", "it", "Vow_T")
    f.addTransition("q2_DLTI", "u", "iu", "Vow_Vow")
    f.addTransition("q2_DLTI", "v", "iv", "Vow_Con")
    f.addTransition("q2_DLTI", "w", "iw", "Vow_Con")
    f.addTransition("q2_DLTI", "x", "ix", "Vow_Con")
    f.addTransition("q2_DLTI", "y", "iy", "Vow_Con")
    f.addTransition("q2_DLTI", "z", "iz", "Vow_Con")

    f.addTransition("Con_Vow","","ing","q_ing")
    f.addSetTransition("Con_Vow",CONS-N-P-T-R,"Vow_Con");
    f.addSetTransition("Con_Vow", N, "Vow_N");
    f.addSetTransition("Con_Vow", P, "Vow_P");
    f.addSetTransition("Con_Vow", T, "Vow_T");
    f.addSetTransition("Con_Vow", R, "Vow_R");
    f.addSetTransition("Con_Vow",VOWS - E,"Vow_Vow")
    f.addTransition("Con_Vow","e","","Vow_Vow")

    f.addTransition("Con_U","e","","U_E")
    f.addSetTransition("Con_U",VOWS - E,"U_Vow")
    f.addSetTransition("Con_U",N,"Vow_N")
    f.addSetTransition("Con_U", P, "Vow_P")
    f.addSetTransition("Con_U", T, "Vow_T")
    f.addSetTransition("Con_U", R, "Vow_R")
    f.addSetTransition("Con_U", CONS - N - P - T - R, "Vow_Con");

    f.addTransition("Con_E", "","ing", "q_ing")
    f.addTransition("Con_E", "a","ea","Vow_Vow")
    f.addTransition("Con_E", "b", "eb", "Vow_Con")
    f.addTransition("Con_E", "c", "ec", "Vow_Con")
    f.addTransition("Con_E", "d", "ed", "Vow_Vow")
    f.addTransition("Con_E", "e", "ee", "Vow_Vow")
    f.addTransition("Con_E", "f", "ef", "Vow_Con")
    f.addTransition("Con_E", "g", "eg", "Vow_Con")
    f.addTransition("Con_E", "h", "eh", "Vow_Con")
    f.addTransition("Con_E", "i", "ei","Vow_Vow")
    f.addTransition("Con_E", "j", "ej", "Vow_Con")
    f.addTransition("Con_E", "k", "ek", "Vow_Con")
    f.addTransition("Con_E", "l", "el", "Vow_Con")
    f.addTransition("Con_E", "m", "em", "Vow_Con")
    f.addTransition("Con_E", "n", "en", "E_N")
    f.addTransition("Con_E", "o", "eo", "Vow_Vow")
    f.addTransition("Con_E", "p", "ep", "Vow_P")
    f.addTransition("Con_E", "q", "eq", "Vow_Con")
    f.addTransition("Con_E", "r", "er", "E_R")
    f.addTransition("Con_E", "s", "es", "Vow_Con")
    f.addTransition("Con_E", "t", "et", "Vow_T")
    f.addTransition("Con_E", "u", "eu", "Vow_Vow")
    f.addTransition("Con_E", "v", "ev", "Vow_Con")
    f.addTransition("Con_E", "w", "ew", "Vow_Con")
    f.addTransition("Con_E", "x", "ex", "Vow_Con")
    f.addTransition("Con_E", "y", "ey", "Vow_Con")
    f.addTransition("Con_E", "z", "ez", "Vow_Con")

    f.addTransition("U_E","","ing","q_ing")

    f.addTransition("U_E","","ing","q_ing")
    f.addSetTransition("U_Vow",E,"U_E")
    f.addSetTransition("U_Vow",CONS,"Vow_Con")

    f.addTransition("Vow_Vow","","ing","q_ing")
    f.addSetTransition("Vow_Vow",VOWS-E,"Vow_Vow")
    f.addSetTransition("Vow_Vow",CONS,"Vow_Con")

    f.addTransition("Vow_E","","ing","q_ing")
    f.addSetTransition("Vow_E",E,"Vow_E")
    f.addSetTransition("Vow_E",VOWS-E,"Vow_E")
    f.addSetTransition("Vow_E",CONS,"Vow_Con")

    f.addTransition("Con_Con","","ing","q_ing")
    f.addTransition("Con_Con","e","","Con_E")
    f.addSetTransition("Con_Con",VOWS-E,"Con_Vow")
    f.addSetTransition("Con_Con",CONS,"Con_Con")

    f.addTransition("Vow_Con","","ing","q_ing")
    f.addSetTransition("Vow_Con",CONS,"Con_Con")
    f.addSetTransition("Vow_Con",VOWS-E,"Con_Vow")
    f.addTransition("Vow_Con","e","","Con_E")

    f.addTransition("E_N","","ing","q_ing")
    f.addSetTransition("E_N",VOWS-E,"Con_Vow")
    f.addTransition("E_N","e","","Con_E")
    f.addSetTransition("E_N",CONS,"Con_Con")

    f.addTransition("Vow_N","","ning", "q_ing")
    f.addSetTransition("Vow_N", VOWS - E, "Con_Vow")
    f.addTransition("Vow_N", "e", "", "Con_E")
    f.addSetTransition("Vow_N", CONS, "Con_Con")

    f.addTransition("E_R","","ing", "q_ing")
    f.addSetTransition("E_R", VOWS - E, "Con_Vow")
    f.addTransition("E_R", "e", "", "Con_E")
    f.addSetTransition("E_R", CONS, "Con_Con")

    f.addTransition("Vow_R","","ring", "q_ing")
    f.addSetTransition("Vow_R", VOWS - E, "Con_Vow")
    f.addTransition("Vow_R", "e", "", "Con_E")
    f.addSetTransition("Vow_R", CONS, "Con_Con")

    f.addTransition("Vow_T","", "ting", "q_ing")
    f.addSetTransition("Vow_T", VOWS - E, "Con_Vow")
    f.addTransition("Vow_T", "e", "", "Con_E")
    f.addSetTransition("Vow_T", CONS, "Con_Con")

    f.addTransition("Vow_P","", "ping", "q_ing")
    f.addSetTransition("Vow_P", VOWS - E, "Con_Vow")
    f.addTransition("Vow_P", "e", "", "Con_E")
    f.addSetTransition("Vow_P", CONS, "Con_Con")

    f.addTransition("q_ing", "", "", "q_EOW")
    return f

if __name__ == "__main__":
    # Pass in the input file as an argument
    if len(sys.argv) < 2:
        print("This script must be given the name of a file containing verbs as an argument")
        quit()
    else:
        file = sys.argv[1]
    #endif

    # Construct an FST for translating verb forms 
    # (Currently constructs a rudimentary, buggy FST; your task is to implement a better one.
    f = buildFST2()
    #f.printFST()
    # Print out the FST translations of the input file
    f.parseInputFile(file)
