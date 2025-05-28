
import { UsageBarChart } from "./UsageBarChart"
import { UsageTable } from "./UsageTable"
import { useQuery } from "@tanstack/react-query"


export interface Usage {
    message_id: number
    timestamp: string
    report_name?: string
    credits_used: number
}

interface UsageResponse {
    usage: Usage[]
}


export const UsageDashboard = () => {
    const { isPending, error, data } = useQuery<UsageResponse>({
    queryKey: ['usageData'],
    queryFn: () =>
      fetch('http://127.0.0.1:8000/usage').then((res) =>
        res.json(),
      ),
    })

    if (isPending) {
        return <div>Fetching the current billing period usage data..</div>;
    }

    if (error) {
        return <div>There is an error: {error.message}</div>;
    }

    return (
      <div className="dashboard">
        <h2>Credit usage Dashboard</h2>
        <UsageBarChart usages={data.usage} />
        <p>You can only sort either Report Name or Credit Used column.</p>
        <UsageTable usages={data.usage} />
      </div>
    );
}
