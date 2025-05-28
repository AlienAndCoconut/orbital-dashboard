import {useMemo} from "react";

import type { Usage } from "./UsageDashboard";
import { BarChart } from "@mui/x-charts/BarChart";

type BarChartProps = {
  usages: Usage[];
};

export const UsageBarChart = ({ usages }: BarChartProps) => {
  const totalCreditsUsedByDate = useMemo(() => {
    const dateCostMap = new Map<string, number>();

    for (const usage of usages) {
      // We extract only the date for example 2024-04-29T02:08:29.375Z -> 2024-04-29
      // And create a map where key is the date and the total credit used as value
      const date = usage.timestamp.split("T")[0];
      const credit_used = usage.credits_used;
      dateCostMap.set(date, (dateCostMap.get(date) || 0) + credit_used);
    }

    // Now we convert it to an array and sort it by earliest to latest date
    return Array.from(dateCostMap.entries()).sort((a, b) =>
      a[0].localeCompare(b[0])
    );
  }, [usages]); // This will only compute when usages change to avoid unnecessary calculations during re-renders

  const dateLabels = totalCreditsUsedByDate.map(item => item[0]);
  const costs = totalCreditsUsedByDate.map(item => item[1]);

  return (
      <BarChart
        height={250}
        width={800}
        series={[
          { data: costs, label: "Total Credits Used", id: "total-credits-used" },
        ]}
        xAxis={[{ data: dateLabels }]}
        yAxis={[{ width: 50 }]}
        colors={["orange"]}
      />
  );
};
