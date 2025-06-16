import pcbnew
import wx

class RenameRuleAreasPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Rename Selected Rule Areas"
        self.category = "Custom Scripts"
        self.description = "Renames selected rule areas with a user-defined sheet name and sequential count."
        self.show_toolbar_button = True

    def Run(self):
        board = pcbnew.GetBoard()
        selected_zones = [zone for zone in board.Zones() if zone.IsSelected() and zone.GetIsRuleArea()]

        if not selected_zones:
            wx.MessageBox("No rule areas selected.", "Error", wx.OK | wx.ICON_ERROR)
            return

        dlg = wx.TextEntryDialog(None, "Enter sheet name:", "Sheet Name", "")
        if dlg.ShowModal() == wx.ID_OK:
            sheet_name = dlg.GetValue().strip()
            if sheet_name:
                # Sort rule areas by Y (top to bottom), then X (left to right)
                selected_zones.sort(key=lambda z: (z.GetPosition().y, z.GetPosition().x))
                for i, zone in enumerate(selected_zones):
                    zone.SetRuleAreaPlacementSource(f"/{sheet_name}_{i+1}/")
                    zone.SetRuleAreaPlacementEnabled(True)
                wx.MessageBox(f"Renamed {len(selected_zones)} rule areas.", "Success", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("Sheet name cannot be empty.", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

RenameRuleAreasPlugin().register()
