const express = require("express");
const cors = require("cors");
const app = express();
const newsRoutes = require("./routes/newsRoutes");

app.use(cors());
app.use("/api/news", newsRoutes);

// ✅ Optional: only run syncToElastic.js if ENABLE_SYNC=true
if (process.env.ENABLE_SYNC === "true") {
  require("./syncToElastic"); // Runs only in dev/local when needed
}

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
