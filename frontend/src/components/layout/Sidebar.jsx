import {
  Activity,
  ArrowLeft,
  BookOpen,
  Box,
  Folder,
  Globe2,
  History,
  Layers3,
  Menu,
  Plus,
  Settings2,
} from "lucide-react"
import RequestExplorer from "../requests/RequestExplorer.jsx"

const navigation = [
  { label: "Overview", icon: Layers3 },
  { label: "Collections", icon: Folder },
  { label: "APIs", icon: Globe2 },
  { label: "Environments", icon: Box },
  { label: "History", icon: History },
  { label: "Documentation", icon: BookOpen },
  { label: "Workflows", icon: Activity },
  { label: "Settings", icon: Settings2 },
]

function Sidebar({ activeSection, collapsed, onNavigate, onToggle, onNotice }) {
  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
      <div className="sidebar-heading">
        {!collapsed && <span>WORKSPACE</span>}
        <button className="sidebar-toggle icon-button" aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"} onClick={onToggle}>
          {collapsed ? <Menu size={17} /> : <ArrowLeft size={16} />}
        </button>
      </div>
      <nav className="main-navigation" aria-label="Main navigation">
        {navigation.map(({ label, icon: Icon }) => (
          <button
            key={label}
            className={`navigation-item ${activeSection === label ? "active" : ""}`}
            aria-current={activeSection === label ? "page" : undefined}
            title={collapsed ? label : undefined}
            onClick={() => onNavigate(label)}
          >
            <Icon size={17} strokeWidth={1.8} />
            {!collapsed && <span>{label}</span>}
          </button>
        ))}
      </nav>
      {!collapsed && (
        <>
          <div className="sidebar-section-title">
            <span>COLLECTIONS</span>
            <button className="subtle-icon-button" aria-label="Add collection" title="Add collection" onClick={() => onNotice("Collection creation is not implemented yet.")}>
              <Plus size={15} />
            </button>
          </div>
          <RequestExplorer />
          <div className="sidebar-footer">
            <button className="help-link" onClick={() => onNotice("Help and feedback are not implemented yet.")}>
              <BookOpen size={15} /><span>Help &amp; feedback</span>
            </button>
            <div className="storage-status">No workspace selected</div>
          </div>
        </>
      )}
    </aside>
  )
}

export default Sidebar
