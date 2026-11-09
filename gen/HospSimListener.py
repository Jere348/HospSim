# Generated from HospSim.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .HospSimParser import HospSimParser
else:
    from HospSimParser import HospSimParser

# This class defines a complete listener for a parse tree produced by HospSimParser.
class HospSimListener(ParseTreeListener):

    # Enter a parse tree produced by HospSimParser#program.
    def enterProgram(self, ctx:HospSimParser.ProgramContext):
        pass

    # Exit a parse tree produced by HospSimParser#program.
    def exitProgram(self, ctx:HospSimParser.ProgramContext):
        pass


    # Enter a parse tree produced by HospSimParser#statement.
    def enterStatement(self, ctx:HospSimParser.StatementContext):
        pass

    # Exit a parse tree produced by HospSimParser#statement.
    def exitStatement(self, ctx:HospSimParser.StatementContext):
        pass


    # Enter a parse tree produced by HospSimParser#resourceDecl.
    def enterResourceDecl(self, ctx:HospSimParser.ResourceDeclContext):
        pass

    # Exit a parse tree produced by HospSimParser#resourceDecl.
    def exitResourceDecl(self, ctx:HospSimParser.ResourceDeclContext):
        pass


    # Enter a parse tree produced by HospSimParser#processDecl.
    def enterProcessDecl(self, ctx:HospSimParser.ProcessDeclContext):
        pass

    # Exit a parse tree produced by HospSimParser#processDecl.
    def exitProcessDecl(self, ctx:HospSimParser.ProcessDeclContext):
        pass


    # Enter a parse tree produced by HospSimParser#stageStmt.
    def enterStageStmt(self, ctx:HospSimParser.StageStmtContext):
        pass

    # Exit a parse tree produced by HospSimParser#stageStmt.
    def exitStageStmt(self, ctx:HospSimParser.StageStmtContext):
        pass


    # Enter a parse tree produced by HospSimParser#arrivalStmt.
    def enterArrivalStmt(self, ctx:HospSimParser.ArrivalStmtContext):
        pass

    # Exit a parse tree produced by HospSimParser#arrivalStmt.
    def exitArrivalStmt(self, ctx:HospSimParser.ArrivalStmtContext):
        pass


    # Enter a parse tree produced by HospSimParser#simulateStmt.
    def enterSimulateStmt(self, ctx:HospSimParser.SimulateStmtContext):
        pass

    # Exit a parse tree produced by HospSimParser#simulateStmt.
    def exitSimulateStmt(self, ctx:HospSimParser.SimulateStmtContext):
        pass


    # Enter a parse tree produced by HospSimParser#showStmt.
    def enterShowStmt(self, ctx:HospSimParser.ShowStmtContext):
        pass

    # Exit a parse tree produced by HospSimParser#showStmt.
    def exitShowStmt(self, ctx:HospSimParser.ShowStmtContext):
        pass


    # Enter a parse tree produced by HospSimParser#TermExpr.
    def enterTermExpr(self, ctx:HospSimParser.TermExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#TermExpr.
    def exitTermExpr(self, ctx:HospSimParser.TermExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#AddExpr.
    def enterAddExpr(self, ctx:HospSimParser.AddExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#AddExpr.
    def exitAddExpr(self, ctx:HospSimParser.AddExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#MultExpr.
    def enterMultExpr(self, ctx:HospSimParser.MultExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#MultExpr.
    def exitMultExpr(self, ctx:HospSimParser.MultExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#FactorExpr.
    def enterFactorExpr(self, ctx:HospSimParser.FactorExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#FactorExpr.
    def exitFactorExpr(self, ctx:HospSimParser.FactorExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#NumExpr.
    def enterNumExpr(self, ctx:HospSimParser.NumExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#NumExpr.
    def exitNumExpr(self, ctx:HospSimParser.NumExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#IdExpr.
    def enterIdExpr(self, ctx:HospSimParser.IdExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#IdExpr.
    def exitIdExpr(self, ctx:HospSimParser.IdExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#ParenExpr.
    def enterParenExpr(self, ctx:HospSimParser.ParenExprContext):
        pass

    # Exit a parse tree produced by HospSimParser#ParenExpr.
    def exitParenExpr(self, ctx:HospSimParser.ParenExprContext):
        pass


    # Enter a parse tree produced by HospSimParser#timeUnit.
    def enterTimeUnit(self, ctx:HospSimParser.TimeUnitContext):
        pass

    # Exit a parse tree produced by HospSimParser#timeUnit.
    def exitTimeUnit(self, ctx:HospSimParser.TimeUnitContext):
        pass



del HospSimParser