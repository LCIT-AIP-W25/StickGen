export const stripHtml = (html: string): string => {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
  };
  export const getSentimentColor = (sentiment: string) => {
    switch (sentiment?.toLowerCase()) {
        case "positive":
            return "bg-success";
        case "negative":
            return "bg-danger";
        case "neutral":
        default:
            return "bg-secondary";
    }
};
