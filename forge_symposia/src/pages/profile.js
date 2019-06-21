import React from 'react';
import styled from 'styled-components';
import useAsyncFn from 'react-use/lib/useAsyncFn';
import useAsync from 'react-use/lib/useAsync';
import useToggle from 'react-use/lib/useToggle';
import { fromUnitToToken } from '@arcblock/forge-util';

import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import Auth from '@arcblock/react-forge/lib/Auth';
import Avatar from '@arcblock/react-forge/lib/Avatar';

import Layout from '../components/layout';
import useSession from '../hooks/session';
import forge from '../libs/forge';
import api from '../libs/api';
import { onAuthError, removeToken } from '../libs/auth';
import Card from '@material-ui/core/Card/Card';
import CardActionArea from '@material-ui/core/CardActionArea/CardActionArea';
import CardMedia from '@material-ui/core/CardMedia/CardMedia';
import CardContent from '@material-ui/core/CardContent/CardContent';
import PageHeader from '../components/page_header';

const renderChunks = chunks => (
  <section className="section">
    <div className="section demos">
      {chunks.map(events => renderExampleCard(events))}
    </div>
  </section>
);

const renderExampleCard = x => (
  <Card key={x.title} className="demo">
    <CardActionArea>
      <CardMedia className="event-pic" image={x.img_url} title={x.title} />
      <CardContent>
        <Typography gutterBottom variant="h5" component="h2">
          {x.title}
        </Typography>
      </CardContent>
    </CardActionArea>
  </Card>
);

export default function ProfilePage() {
  const state = useSession();
  const [isFetched, setFetched] = useToggle(false);
  const [isOpen, setOpen] = useToggle(false);
  const [balance, fetchBalance] = useAsyncFn(async () => {
    if (state.value && state.value.user) {
      const address = state.value.user.did.replace(/^did:abt:/, '');
      const [{ state: account }, { state: chain }] = await Promise.all([
        forge.getAccountState({ address }),
        forge.getForgeState({}, { ignoreFields: ['state.protocols'] }),
      ]);

      return {
        account,
        token: chain.token,
      };
    }

    return null;
  }, [state.value]);

  const ticket_state = useAsync(async () => {
    if (state.value && state.value.user) {
      const address = state.value.user.did.replace(/^did:abt:/, '');
      return await Promise.all([api.get(`/api/list_tickets/${address}`)]);
    }

    return null;
  }, [state.value]);

  const onLogout = () => {
    removeToken();
    window.location.href = '/';
  };

  if (state.loading || !state.value) {
    return (
      <Layout title="Profile">
        <Main>
          <CircularProgress />
        </Main>
      </Layout>
    );
  }

  if (state.error) {
    return (
      <Layout title="Profile">
        <Main>{state.error.message}</Main>
      </Layout>
    );
  }

  if (!state.value.user) {
    window.location.href = '/?openLogin=true';
    return null;
  }

  if (ticket_state.loading || !ticket_state.value) {
    return (
      <Layout title="Profile">
        <Main>
          <CircularProgress />
        </Main>
      </Layout>
    );
  }
  console.log(ticket_state);

  const ticket_chunks = ticket_state.value[0].data;

  if (!isFetched) {
    setTimeout(() => {
      setFetched(true);
      fetchBalance();
    }, 100);
  }

  return (
    <Layout title="Profile">
      <Main>
        <Grid container spacing={40}>
          <Grid item xs={12} md={3} className="avatar">
            <Avatar size={240} did={state.value.user.did} />
            <Button color="secondary" variant="outlined" onClick={onLogout}>
              Logout
            </Button>
            <Button
              color="primary"
              variant="outlined"
              href="/payment"
              style={{ marginTop: '30px' }}
            >
              My Purchase
            </Button>
            {balance.value && balance.value.account && (
              <Button
                color="primary"
                variant="contained"
                onClick={() => setOpen()}
                style={{ marginTop: '30px' }}
              >
                Get 25 TBA
              </Button>
            )}
          </Grid>
          <Grid item xs={12} md={8} className="meta">
            <Typography component="h3" variant="h4">
              My Profile
            </Typography>
            <List>
              <ListItem className="meta-item">
                <ListItemText primary={state.value.user.did} secondary="DID" />
              </ListItem>
              <ListItem className="meta-item">
                <ListItemText
                  primary={state.value.user.name || '-'}
                  secondary="Name"
                />
              </ListItem>
              <ListItem className="meta-item">
                <ListItemText
                  primary={state.value.user.email || '-'}
                  secondary="Email"
                />
              </ListItem>
              <ListItem className="meta-item">
                <ListItemText
                  primary={state.value.user.mobile || '-'}
                  secondary="Phone"
                />
              </ListItem>
              <ListItem className="meta-item">
                <ListItemText
                  primary={
                    balance.value &&
                    balance.value.account &&
                    balance.value.token ? (
                      `${fromUnitToToken(
                        balance.value.account.balance,
                        balance.value.token.decimal
                      )} ${balance.value.token.symbol}`
                    ) : (
                      <CircularProgress size={18} />
                    )
                  }
                  secondary="Account Balance"
                />
              </ListItem>
              <ListItem className="meta-item" />
            </List>
          </Grid>
        </Grid>
        <section className="section">
          <PageHeader title="Tickets" />
          <div>{ticket_chunks.map(x => renderChunks(x))}</div>
        </section>
      </Main>
      {isOpen && (
        <Auth
          responsive
          action="checkin"
          checkFn={api.get}
          onError={onAuthError}
          onClose={() => setOpen()}
          onSuccess={() => window.location.reload()}
          messages={{
            title: 'Get 25 TBA for FREE',
            scan: 'Scan qrcode to get 25 TBA for FREE',
            confirm: 'Confirm on your ABT Wallet',
            success: '25 TBA sent to your account',
          }}
        />
      )}
    </Layout>
  );
}

const Main = styled.main`
  margin: 100px 100px 100px;

  .avatar {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-center;

    svg {
      margin-bottom: 40px;
    }
  }

  .meta {
    display: flex;
    flex-grow: 1;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
  }

  .meta-item {
    padding-left: 0;
  }

  .section {
    margin-top: 100px;

    margin-bottom: 50px;
    .section__header {
      margin-bottom: 20px;
    }
  }

  .demos {
    display: flex;
    justify-content: space-around;
    align-items: center;

    .demo {
      width: 30%;

      .event-pic {
        height: 140px;
      }
    }
  }
`;
