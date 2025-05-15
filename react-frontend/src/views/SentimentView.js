import React, { useEffect, useState } from "react";
import {
  Badge,
  Card,
  Table,
  Container,
  Row,
  Col,
  Spinner,
  Alert,
} from "react-bootstrap";

import { fetchSentimentData } from "services/apiService";

const parseSummaryString = (summary) => {
  const lines = summary.trim().split("\n");
  const parsed = {};
  lines.forEach((line) => {
    if (line.startsWith("Date Today:"))
      parsed.dateToday = line.replace("Date Today: ", "").trim();
    else if (line.startsWith("Total Analyzed Posts:"))
      parsed.totalAnalyzedPosts = line
        .replace("Total Analyzed Posts: ", "")
        .trim();
    else if (line.startsWith("Bullish:"))
      parsed.bullish = line.replace("Bullish: ", "").trim();
    else if (line.startsWith("Neutral:"))
      parsed.neutral = line.replace("Neutral: ", "").trim();
    else if (line.startsWith("Bearish:"))
      parsed.bearish = line.replace("Bearish: ", "").trim();
    else if (
      line.trim() !== "" &&
      !Object.values(parsed).includes(line.trim())
    ) {
      parsed.overallSentiment = line.trim();
    }
  });
  if (!parsed.overallSentiment && lines.length > 0) {
    const lastNonEmptyLine = [...lines]
      .reverse()
      .find((line) => line.trim() !== "");
    if (
      lastNonEmptyLine &&
      !Object.values(parsed).includes(lastNonEmptyLine.trim())
    ) {
      parsed.overallSentiment = lastNonEmptyLine.trim();
    }
  }
  return parsed;
};

function SentimentView() {
  const [apiResponse, setApiResponse] = useState(null);
  const [parsedSummary, setParsedSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchSentimentData(); 
        setApiResponse(data); 
        if (data && data.summary) {
          setParsedSummary(parseSummaryString(data.summary));
        } else {
          setParsedSummary({});
        }
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "An unknown error occurred"
        );
        console.error("Failed to fetch sentiment data:", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (
    !apiResponse ||
    !apiResponse.data ||
    !apiResponse.sources ||
    !parsedSummary
  ) {
    return (
      <Container fluid>
        <Alert variant="warning" className="mt-3">
          No sentiment data available or data is incomplete.
        </Alert>
      </Container>
    );
  }

  const { summary, data: sentimentDetails, sources } = apiResponse;

  const getSentimentVariant = (sentiment) => {
    if (!sentiment) return "secondary";
    const s = sentiment.toLowerCase();
    if (s.includes("bull")) return "success";
    if (s.includes("bear")) return "danger";
    if (s.includes("neutral")) return "warning";
    return "secondary";
  };

  const mostCommonSentimentText = sentimentDetails.most_common
    ? sentimentDetails.most_common.charAt(0).toUpperCase() +
      sentimentDetails.most_common.slice(1)
    : "N/A";

  return (
    <Container fluid>
      <Row>
        <Col md="12">
          <Card>
            <Card.Header>
              <Card.Title as="h4">Sentiment Analysis Summary</Card.Title>
              <p className="card-category">
                {parsedSummary.dateToday
                  ? `Data for: ${parsedSummary.dateToday}`
                  : "Latest Data"}
              </p>
            </Card.Header>
            <Card.Body>
              {parsedSummary.totalAnalyzedPosts && (
                <p>
                  <strong>Total Analyzed Posts:</strong>{" "}
                  {parsedSummary.totalAnalyzedPosts}
                </p>
              )}
              {parsedSummary.bullish && (
                <p>
                  <strong>Bullish:</strong>{" "}
                  <span className={`text-${getSentimentVariant("bullish")}`}>
                    {parsedSummary.bullish}
                  </span>
                </p>
              )}
              {parsedSummary.neutral && (
                <p>
                  <strong>Neutral:</strong>{" "}
                  <span className={`text-${getSentimentVariant("neutral")}`}>
                    {parsedSummary.neutral}
                  </span>
                </p>
              )}
              {parsedSummary.bearish && (
                <p>
                  <strong>Bearish:</strong>{" "}
                  <span className={`text-${getSentimentVariant("bearish")}`}>
                    {parsedSummary.bearish}
                  </span>
                </p>
              )}
              {parsedSummary.overallSentiment && (
                <p className="mt-3">
                  <em>{parsedSummary.overallSentiment}</em>
                </p>
              )}
              {sentimentDetails.most_common && (
                <p className="mt-2">
                  <strong>Most Common Sentiment:</strong>{" "}
                  <Badge
                    pill
                    bg={getSentimentVariant(sentimentDetails.most_common)}
                  >
                    {mostCommonSentimentText}
                  </Badge>
                </p>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        {}
        <Col lg="3" sm="6">
          <Card className="card-stats">
            <Card.Body>
              <Row>
                <Col xs="5">
                  <div className="icon-big text-center icon-warning">
                    <i className="nc-icon nc-chart text-warning"></i>
                  </div>
                </Col>
                <Col xs="7">
                  <div className="numbers">
                    <p className="card-category">Total Analyzed</p>
                    <Card.Title as="h4">
                      {sentimentDetails.total_analyzed}
                    </Card.Title>
                  </div>
                </Col>
              </Row>
            </Card.Body>
            <Card.Footer>
              <hr />
              <div className="stats">
                <i className="fas fa-database mr-1"></i>All sources
              </div>
            </Card.Footer>
          </Card>
        </Col>
        <Col lg="3" sm="6">
          <Card className="card-stats">
            <Card.Body>
              <Row>
                <Col xs="5">
                  <div
                    className={`icon-big text-center icon-${getSentimentVariant(
                      "bullish"
                    )}`}
                  >
                    <i
                      className={`nc-icon nc-chart-bar-32 text-${getSentimentVariant(
                        "bullish"
                      )}`}
                    ></i>
                  </div>
                </Col>
                <Col xs="7">
                  <div className="numbers">
                    <p className="card-category">Bullish Posts</p>
                    <Card.Title as="h4">{sentimentDetails.bull}</Card.Title>
                  </div>
                </Col>
              </Row>
            </Card.Body>
            <Card.Footer>
              <hr />
              <div className="stats">
                <i className="fas fa-percent mr-1"></i>
                {sentimentDetails.total_analyzed > 0
                  ? (
                      (sentimentDetails.bull /
                        sentimentDetails.total_analyzed) *
                      100
                    ).toFixed(1)
                  : 0}
                %
              </div>
            </Card.Footer>
          </Card>
        </Col>
        <Col lg="3" sm="6">
          <Card className="card-stats">
            <Card.Body>
              <Row>
                <Col xs="5">
                  <div
                    className={`icon-big text-center icon-${getSentimentVariant(
                      "neutral"
                    )}`}
                  >
                    <i
                      className={`nc-icon nc-vector text-${getSentimentVariant(
                        "neutral"
                      )}`}
                    ></i>
                  </div>
                </Col>
                <Col xs="7">
                  <div className="numbers">
                    <p className="card-category">Neutral Posts</p>
                    <Card.Title as="h4">{sentimentDetails.neutral}</Card.Title>
                  </div>
                </Col>
              </Row>
            </Card.Body>
            <Card.Footer>
              <hr />
              <div className="stats">
                <i className="fas fa-percent mr-1"></i>
                {sentimentDetails.total_analyzed > 0
                  ? (
                      (sentimentDetails.neutral /
                        sentimentDetails.total_analyzed) *
                      100
                    ).toFixed(1)
                  : 0}
                %
              </div>
            </Card.Footer>
          </Card>
        </Col>
        <Col lg="3" sm="6">
          <Card className="card-stats">
            <Card.Body>
              <Row>
                <Col xs="5">
                  <div
                    className={`icon-big text-center icon-${getSentimentVariant(
                      "bearish"
                    )}`}
                  >
                    <i
                      className={`nc-icon nc-zoom-split text-${getSentimentVariant(
                        "bearish"
                      )}`}
                    ></i>
                  </div>
                </Col>
                <Col xs="7">
                  <div className="numbers">
                    <p className="card-category">Bearish Posts</p>
                    <Card.Title as="h4">{sentimentDetails.bear}</Card.Title>
                  </div>
                </Col>
              </Row>
            </Card.Body>
            <Card.Footer>
              <hr />
              <div className="stats">
                <i className="fas fa-percent mr-1"></i>
                {sentimentDetails.total_analyzed > 0
                  ? (
                      (sentimentDetails.bear /
                        sentimentDetails.total_analyzed) *
                      100
                    ).toFixed(1)
                  : 0}
                %
              </div>
            </Card.Footer>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md="12">
          <Card className="strpied-tabled-with-hover">
            <Card.Header>
              <Card.Title as="h4">Data Sources</Card.Title>
              <p className="card-category">
                Platforms and channels included in analysis
              </p>
            </Card.Header>
            <Card.Body className="table-full-width table-responsive px-0">
              {}
              {sources && Array.isArray(sources) && sources.length > 0 ? (
                <Table className="table-hover table-striped">
                  <thead>
                    <tr>
                      <th className="border-0">ID</th>
                      <th className="border-0">Platform</th>
                      <th className="border-0">Channel</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sources.map(
                      (
                        source,
                        index 
                      ) => (
                        <tr key={source.channel || index}>
                          {" "}
                          {}
                          <td>{index + 1}</td>
                          <td>{source.platform}</td>
                          <td>{source.channel}</td>
                        </tr>
                      )
                    )}
                  </tbody>
                </Table>
              ) : (
                <div className="p-3 text-muted">No source data available.</div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default SentimentView;
