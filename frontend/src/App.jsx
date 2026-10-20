import { useState } from "react"
import { X } from "lucide-react"
import AppLayout from "./components/layout/AppLayout.jsx"
import DashboardPage from "./pages/DashboardPage.jsx"
import RequestWorkspacePage from "./pages/RequestWorkspacePage.jsx"
import EmptyState from "./components/common/EmptyState.jsx"
import Modal from "./components/common/Modal.jsx"

function App() {
  const [activeSection, setActiveSection] = useState("Overview")
  const [collapsed, setCollapsed] = useState(false)
  const [showRequestWorkspace, setShowRequestWorkspace] = useState(false)
  const [modalType, setModalType] = useState(null)
  const [notice, setNotice] = useState("")

  const openRequestWorkspace = () => {
    setShowRequestWorkspace(true)
    setActiveSection("Collections")
  }

  const navigate = (section) => {
    setActiveSection(section)
    setShowRequestWorkspace(false)
  }

  let page
  if (showRequestWorkspace) {
    page = <RequestWorkspacePage onBack={() => navigate("Overview")} onNotice={setNotice} />
  } else if (activeSection === "Overview") {
    page = <DashboardPage onCreateRequest={openRequestWorkspace} onOpenModal={setModalType} />
  } else {
    const messages = {
      Collections: ["No collections yet", "Your collections will appear here when they are available."],
      APIs: ["Not implemented yet", "API definitions are not available in this frontend preview."],
      Environments: ["No environments available", "Environments will appear here when they are available."],
      History: ["No recent activity", "Your recent requests will appear here."],
      Documentation: ["No documentation yet", "Documentation will appear here when it is available."],
      Workflows: ["Not implemented yet", "Workflow management is not available in this frontend preview."],
      Settings: ["Not implemented yet", "Settings are not available in this frontend preview."],
    }
    const [title, description] = messages[activeSection] ?? ["Nothing here yet", "This section is not available yet."]
    page = <EmptyState title={title} description={description} />
  }

  return (
    <>
      <AppLayout
        activeSection={activeSection}
        collapsed={collapsed}
        onNavigate={navigate}
        onToggleSidebar={() => setCollapsed((value) => !value)}
        onNotice={setNotice}
      >
        {page}
      </AppLayout>
      {notice && (
        <div className="notice" role="status">
          <span>{notice}</span>
          <button className="notice-dismiss" aria-label="Dismiss notification" onClick={() => setNotice("")}><X size={14} /></button>
        </div>
      )}
      {modalType && <Modal type={modalType} onClose={() => setModalType(null)} />}
    </>
  )
}

export default App
