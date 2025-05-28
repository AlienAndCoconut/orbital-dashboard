import { useState, useEffect, useMemo } from "react";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";
import type { GridColDef } from "@mui/x-data-grid";
import type { Usage } from "./UsageDashboard";
import { useSearchParams } from "react-router-dom";

const usageColumnHeader: GridColDef<(typeof rows)[number]>[] = [
  { field: "id", headerName: "Message ID", width: 100, sortable: false },
  {
    field: "timestamp",
    headerName: "Timestamp",
    width: 200,
    sortable: false,
  },
  {
    field: "reportName",
    headerName: "Report Name",
    width: 300,
    sortable: true,
  },
  {
    field: "creditsUsed",
    headerName: "Credits Used",
    type: "number",
    width: 150,
    sortable: true,
  },
];

type SortOrder = "asc" | "desc" | undefined;

type UsageTableProps = {
  usages: Usage[];
};

export const UsageTable = ({ usages }: UsageTableProps) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [sortOrderCreditUsed, setSortOrderCreditUsed] =
    useState<SortOrder>(undefined);
  const [sortOrderReportName, setSortOrderReportName] =
    useState<SortOrder>(undefined);

  // NOTE: you can only sort one of the column at a time
  useEffect(() => {
    const creditUsedSort = searchParams.get("sortCreditUsedOrder");
    if (creditUsedSort === "asc" || creditUsedSort === "desc") {
      setSortOrderCreditUsed(creditUsedSort as SortOrder);
    }

    const reportNameSort = searchParams.get("sortReportNameOrder");
    if (reportNameSort === "asc" || reportNameSort === "desc") {
      setSortOrderReportName(reportNameSort as SortOrder);
    }
  }, [searchParams]); // Whenever the url gets updated - we grab the url params and set the sort order state

  const handleSortOrderCreditUsed = (order?: SortOrder) => {
    setSortOrderReportName(undefined); // Since we can only sort one column at a time, we will always reset the other
    setSortOrderCreditUsed(order);

    // Now we update the URL without re-render
    const newSearchParams = new URLSearchParams(searchParams);
    if (order) {
      newSearchParams.set("sortCreditUsedOrder", order);
      newSearchParams.delete("sortReportNameOrder"); // We remove the other column sort order if it exists on url
    } else {
      newSearchParams.delete("sortCreditUsedOrder");
    }
    setSearchParams(newSearchParams);
  };

  const handleSortOrderReportName = (order?: SortOrder) => {
    setSortOrderCreditUsed(undefined); // Since we can only sort one column at a time, we will always reset the other
    setSortOrderReportName(order);

    const newSearchParams = new URLSearchParams(searchParams);
    if (order) {
      newSearchParams.set("sortReportNameOrder", order);
      newSearchParams.delete("sortCreditUsedOrder");
    } else {
      newSearchParams.delete("sortReportNameOrder");
    }
    setSearchParams(newSearchParams);
  };

  // This function returns the sort configuration for the Credit Used column and Report Name column
  // There are three possible states for each column: "asc", "desc", or undefined (no sorting)
  const sortModelSettings = () => {
    const settings = [];
    if (sortOrderCreditUsed) {
      settings.push({ field: "creditsUsed", sort: sortOrderCreditUsed });
    }
    if (sortOrderReportName) {
      settings.push({ field: "reportName", sort: sortOrderReportName });
    }
    return settings;
  };

  const rows = useMemo(() => 
    usages.map((usage) => ({
      id: usage.message_id,
      timestamp: usage.timestamp.replace("T", " ").split(".")[0].slice(0, -3),
      reportName: usage.report_name || "",
      creditsUsed: usage.credits_used.toFixed(2),
    })), [usages]
  );

  return (
    <Box sx={{ height: "100%", width: "100%" }}>
      <DataGrid
        sortModel={sortModelSettings()}
        rows={rows}
        columns={usageColumnHeader}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 5,
            },
          },
        }}
        pageSizeOptions={[5]}
        onColumnHeaderClick={(params) => {
          // This toggles the sort order for the clicked column
          if (params.field === "creditsUsed") {
            const updatedOrder =
              sortOrderCreditUsed === "asc"
                ? "desc"
                : sortOrderCreditUsed === "desc"
                ? undefined
                : "asc";
            handleSortOrderCreditUsed(updatedOrder)
          }
          if (params.field === "reportName") {
            const updatedOrder =
              sortOrderReportName === "asc"
                ? "desc"
                : sortOrderReportName === "desc"
                ? undefined
                : "asc";
            handleSortOrderReportName(updatedOrder);
          }
        }}
      />
    </Box>
  );
};
