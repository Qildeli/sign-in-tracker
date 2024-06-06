import {Box, Container, Typography} from "@mui/material";

interface AuthProps {
    title: string
    children: any
}

function Auth({ children, title }: AuthProps){
    return (
        <Box sx={{ mt: 16 }}>
            <Container maxWidth="xs">
                <Typography variant="h4" gutterBottom align="center" >
                    { title }
              </Typography>
                <Box>{ children }</Box>
            </Container>
        </Box>
    )
}

export default Auth
