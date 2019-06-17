/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import styled from 'styled-components';

import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';

import Layout from '../components/layout';
import api from "../libs/api";
import useAsync from "react-use/lib/useAsync";
import useToggle from "react-use/lib/useToggle";
import CircularProgress from "@material-ui/core/CircularProgress/CircularProgress";


async function fetchEventList() {
    return await Promise.all([api.get('/api/list_events')]);
}

const renderChunks = chunks => (
    <section className="section">
        <div className="section demos">{chunks.map(events => renderExampleCard(events))}</div>
    </section>

)

const renderExampleCard = x => (
    <Card key={x.title} className="demo">
        <CardActionArea>
            <CardMedia className="event-pic" image={x.img_url} title={x.title}
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="h2">
                    {x.title}
                </Typography>
                <Typography variant="body2" color="textSecondary" component="p">
                    Start Time: {x.start_time}
                </Typography>
                <Typography variant="body2" color="textSecondary" component="p">
                    Location: {x.location}
                </Typography>
            </CardContent>
        </CardActionArea>
        <CardActions>
            <Button component="a" href={`detail?event_address=${x.address}`} size="small" color="primary">
                Details
            </Button>
        </CardActions>
    </Card>
);

export default function EventsPage() {
    const state = useAsync(fetchEventList);

    if (state.loading || !state.value) {
        return (
            <Layout title="Events">
                <Main>
                    <CircularProgress/>
                </Main>
            </Layout>
        );
    }

    if (state.error) {
        return (
            <Layout title="Payment">
                <Main>{state.error.message}</Main>
            </Layout>
        );
    }
    const event_chunks = state.value[0].data
    console.log(event_chunks)

    return (
        <Layout title="Home">
            <Main>
                <Typography component="h2" variant="h4" className="page-header" color="textPrimary">
                    Welcome to Forge Symposia!
                </Typography>
                <section className="section">
                    <div className="section">
                        {event_chunks.map(x => renderChunks(x))}
                        </div>
                </section>
            </Main>
        </Layout>
    );
}
const Main = styled.main`
  margin: 100px 100px 100px;
  

  a {
    color: ${props => props.theme.colors.green};
    text-decoration: none;
  }

  .page-header {
    margin-bottom: 20px;
  }

  .page-description {
    margin-bottom: 30px;
  }

  .section {
    margin-bottom: 50px;
    .section__header {
      margin-bottom: 20px;
    }
  }

  .demos {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .demo {
      width: 30%; 
      
      .event-pic {
         height: 140px;
       }
    }
  }
  
  

`;
