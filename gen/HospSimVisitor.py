# Generated from HospSim.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .HospSimParser import HospSimParser
else:
    from HospSimParser import HospSimParser

# This class defines a complete generic visitor for a parse tree produced by HospSimParser.

class HospSimVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HospSimParser#program.
    def visitProgram(self, ctx:HospSimParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#statement.
    def visitStatement(self, ctx:HospSimParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#resourceDecl.
    def visitResourceDecl(self, ctx:HospSimParser.ResourceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#processDecl.
    def visitProcessDecl(self, ctx:HospSimParser.ProcessDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#stageStmt.
    def visitStageStmt(self, ctx:HospSimParser.StageStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#arrivalStmt.
    def visitArrivalStmt(self, ctx:HospSimParser.ArrivalStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#simulateStmt.
    def visitSimulateStmt(self, ctx:HospSimParser.SimulateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#showStmt.
    def visitShowStmt(self, ctx:HospSimParser.ShowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#TermExpr.
    def visitTermExpr(self, ctx:HospSimParser.TermExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#AddExpr.
    def visitAddExpr(self, ctx:HospSimParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#MultExpr.
    def visitMultExpr(self, ctx:HospSimParser.MultExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#FactorExpr.
    def visitFactorExpr(self, ctx:HospSimParser.FactorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#NumExpr.
    def visitNumExpr(self, ctx:HospSimParser.NumExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#IdExpr.
    def visitIdExpr(self, ctx:HospSimParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#ParenExpr.
    def visitParenExpr(self, ctx:HospSimParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HospSimParser#timeUnit.
    def visitTimeUnit(self, ctx:HospSimParser.TimeUnitContext):
        return self.visitChildren(ctx)



del HospSimParser