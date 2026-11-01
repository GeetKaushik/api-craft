import AppHeader from "./AppHeader.jsx"
import Sidebar from "./Sidebar.jsx"

function AppLayout({ activeSection, collapsed, onNavigate, onToggleSidebar, onNotice, children }) {
  return (
    <div className="app-shell">
      <AppHeader onNotice={onNotice} />
      <div className="app-body">
        <Sidebar
          activeSection={activeSection}
          collapsed={collapsed}
          onNavigate={onNavigate}
          onToggle={onToggleSidebar}
          onNotice={onNotice}
        />
        <main className="main-content">{children}</main>
      </div>
    </div>
  )
}

export default AppLayout
