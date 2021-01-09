import sublime
import sublime_plugin


class UnfoldBeforeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for sel in view.sel():
            # fold the position before the selection
            view.unfold(sublime.Region(sel.b - 1))


class IsBehindFoldContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if key != "is_behind_fold":
            return

        quantor = all if match_all else any

        result = quantor(
            view.is_folded(sel) and view.is_folded(sublime.Region(sel.b - 1))
            for sel in view.sel()
        )

        if operator == sublime.OP_EQUAL:
            result = result == operand
        elif operator == sublime.OP_NOT_EQUAL:
            result = result != operand
        else:
            raise Exception("Operator type not supported")

        return result