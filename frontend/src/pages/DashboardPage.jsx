import WelcomeDashboard from "../features/dashboard/WelcomeDashboard.jsx"

function DashboardPage({ onCreateRequest, onOpenModal }) {
  return <WelcomeDashboard onCreateRequest={onCreateRequest} onOpenModal={onOpenModal} />
}

export default DashboardPage
