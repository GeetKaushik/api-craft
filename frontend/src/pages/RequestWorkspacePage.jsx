import { ArrowLeft, ChevronRight } from "lucide-react"
import RequestEditor from "../features/request-editor/RequestEditor.jsx"
import ResponseViewer from "../components/response/ResponseViewer.jsx"

function RequestWorkspacePage({ onBack, onNotice }) {
  return (
    <div className="request-workspace">
      <div className="breadcrumbs">
        <button onClick={onBack}><ArrowLeft size={15} /> Overview</button>
        <ChevronRight size={14} />
        <span className="breadcrumb-current">New request</span>
      </div>
      <div className="request-title-row">
        <div>
          <span className="request-kicker">UNSAVED DRAFT</span>
          <h1>New request</h1>
        </div>
      </div>
      <RequestEditor onNotice={onNotice} />
      <ResponseViewer />
    </div>
  )
}

export default RequestWorkspacePage
